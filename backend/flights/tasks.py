"""Tareas Celery para scraping, expiración, y notificaciones."""
import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2)
def scrape_single_source(self, source_id):
    """Scrapea una fuente individual."""
    from flights.models import FlightSource
    from flights.scrapers.registry import get_scraper_for_source

    try:
        source = FlightSource.objects.get(id=source_id)
    except FlightSource.DoesNotExist:
        logger.error(f"Fuente {source_id} no encontrada")
        return

    if not source.is_active:
        logger.info(f"Fuente {source.name} inactiva, saltando")
        return

    scraper = get_scraper_for_source(source)
    if not scraper:
        logger.warning(f"No hay scraper para {source.name}")
        return

    try:
        results = scraper.scrape()
        logger.info(f"Scraping {source.name}: {len(results)} resultados")
        return len(results)
    except Exception as e:
        logger.error(f"Error scraping {source.name}: {e}")
        source.record_error(str(e))
        raise self.retry(exc=e, countdown=60)


@shared_task
def scrape_all_sources():
    """Scrapea todas las fuentes activas de tipo web."""
    from flights.models import FlightSource

    sources = FlightSource.objects.filter(
        is_active=True,
        source_type__in=['web_public', 'web_private'],
    )

    total = 0
    for source in sources:
        # Verificar si toca scraping según intervalo
        if source.last_scraped:
            next_scrape = source.last_scraped + timedelta(minutes=source.scrape_interval_minutes)
            if timezone.now() < next_scrape:
                continue

        # Saltar fuentes con muchos errores consecutivos
        if source.consecutive_errors >= 5:
            logger.warning(f"Saltando {source.name}: {source.consecutive_errors} errores consecutivos")
            continue

        scrape_single_source.delay(source.id)
        total += 1

    logger.info(f"Scraping lanzado para {total} fuentes")
    return total


@shared_task
def expire_old_empty_legs():
    """Expira empty legs con fecha pasada."""
    from flights.models import EmptyLeg

    today = timezone.now().date()
    expired = EmptyLeg.objects.filter(
        status='available',
        departure_date__lt=today,
    ).update(status='expired')

    logger.info(f"Expirados {expired} empty legs")
    return expired


@shared_task
def cleanup_old_data():
    """Elimina datos con más de 90 días."""
    from flights.models import EmptyLeg, Flight

    cutoff = timezone.now() - timedelta(days=90)

    deleted_legs = EmptyLeg.objects.filter(
        created_at__lt=cutoff,
        status__in=['expired', 'cancelled'],
    ).delete()[0]

    deleted_flights = Flight.objects.filter(
        created_at__lt=cutoff,
    ).delete()[0]

    logger.info(f"Limpieza: {deleted_legs} legs y {deleted_flights} vuelos eliminados")
    return {'legs': deleted_legs, 'flights': deleted_flights}


@shared_task
def check_new_empty_legs():
    """Chequea legs creados en la última hora y envía alertas inmediatas."""
    from flights.models import EmptyLeg
    from notifications.models import AlertSubscription, NotificationLog
    from notifications.tasks import send_alert_email

    one_hour_ago = timezone.now() - timedelta(hours=1)
    new_legs = EmptyLeg.objects.filter(
        created_at__gte=one_hour_ago,
        published=True,
        status='available',
    )

    if not new_legs.exists():
        return 0

    subscriptions = AlertSubscription.objects.filter(
        is_active=True,
        frequency='immediate',
    )

    sent = 0
    for sub in subscriptions:
        for leg in new_legs:
            if sub.matches_empty_leg(leg):
                # Verificar que no se haya enviado ya
                if not NotificationLog.objects.filter(subscription=sub, empty_leg=leg).exists():
                    send_alert_email.delay(sub.id, leg.id)
                    sent += 1

    logger.info(f"Alertas inmediatas: {sent} enviadas")
    return sent


@shared_task
def send_daily_digest():
    """Envía resumen diario a suscriptores."""
    from flights.models import EmptyLeg
    from notifications.models import AlertSubscription
    from notifications.tasks import send_digest_email

    today = timezone.now().date()
    available_legs = EmptyLeg.objects.filter(
        published=True,
        status='available',
        departure_date__gte=today,
    )

    subscriptions = AlertSubscription.objects.filter(
        is_active=True,
        frequency='daily',
    )

    sent = 0
    for sub in subscriptions:
        matching = [leg for leg in available_legs if sub.matches_empty_leg(leg)]
        if matching:
            send_digest_email.delay(sub.id, [leg.id for leg in matching])
            sent += 1

    logger.info(f"Digest diario: {sent} enviados")
    return sent
