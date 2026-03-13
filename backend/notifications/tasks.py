"""Tareas Celery para notificaciones por email."""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_alert_email(subscription_id, empty_leg_id):
    """Envía email de alerta para un empty leg específico."""
    from notifications.models import AlertSubscription, NotificationLog
    from flights.models import EmptyLeg

    try:
        sub = AlertSubscription.objects.get(id=subscription_id, is_active=True)
        leg = EmptyLeg.objects.get(id=empty_leg_id)
    except (AlertSubscription.DoesNotExist, EmptyLeg.DoesNotExist):
        return

    # Verificar que no se haya enviado ya
    if NotificationLog.objects.filter(subscription=sub, empty_leg=leg).exists():
        return

    subject = f'✈️ Nuevo Empty Leg: {leg.origin_raw} → {leg.destination_raw} — {leg.departure_date}'
    message = (
        f'Hola {sub.name or ""},\n\n'
        f'Hay un nuevo empty leg disponible que coincide con tus criterios:\n\n'
        f'🛫 Ruta: {leg.origin_raw} → {leg.destination_raw}\n'
        f'📅 Fecha: {leg.departure_date}\n'
        f'✈️ Aeronave: {leg.aircraft_raw or "Por confirmar"}\n'
        f'👥 Pasajeros: {leg.max_passengers or "Consultar"}\n\n'
        f'Para más información, visitá nuestra web.\n\n'
        f'— Aerowise\n'
        f'Para desuscribirte, respondé a este email.'
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [sub.email])
        NotificationLog.objects.create(
            subscription=sub,
            empty_leg=leg,
            email_subject=subject,
        )
        logger.info(f"Alerta enviada a {sub.email} para leg {leg.id}")
    except Exception as e:
        logger.error(f"Error enviando alerta a {sub.email}: {e}")


@shared_task
def send_digest_email(subscription_id, empty_leg_ids):
    """Envía resumen de empty legs."""
    from notifications.models import AlertSubscription, NotificationLog
    from flights.models import EmptyLeg

    try:
        sub = AlertSubscription.objects.get(id=subscription_id, is_active=True)
    except AlertSubscription.DoesNotExist:
        return

    legs = EmptyLeg.objects.filter(id__in=empty_leg_ids)
    if not legs:
        return

    subject = f'✈️ Aerowise — {len(legs)} empty legs disponibles'
    lines = [f'Hola {sub.name or ""},\n', f'Estos son los empty legs que coinciden con tus criterios:\n']

    for leg in legs:
        lines.append(f'• {leg.origin_raw} → {leg.destination_raw} — {leg.departure_date} — {leg.aircraft_raw or ""}')
        # Registrar notificación
        NotificationLog.objects.get_or_create(
            subscription=sub,
            empty_leg=leg,
            defaults={'email_subject': subject},
        )

    lines.append(f'\nVisitá nuestra web para más detalles.\n\n— Aerowise')
    message = '\n'.join(lines)

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [sub.email])
        logger.info(f"Digest enviado a {sub.email} con {len(legs)} legs")
    except Exception as e:
        logger.error(f"Error enviando digest a {sub.email}: {e}")
