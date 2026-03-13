"""Comando CLI para ejecutar scrapers."""
from django.core.management.base import BaseCommand
from flights.models import FlightSource
from flights.scrapers.registry import get_scraper_for_source


class Command(BaseCommand):
    help = 'Ejecuta scrapers de empty legs'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, help='Nombre de la fuente a scrapear')
        parser.add_argument('--list', action='store_true', help='Lista fuentes disponibles')

    def handle(self, *args, **options):
        if options['list']:
            sources = FlightSource.objects.filter(is_active=True)
            for s in sources:
                scraper = get_scraper_for_source(s)
                status = '✓' if scraper else '✗'
                self.stdout.write(f"  {status} {s.name} ({s.get_source_type_display()}) — {s.url}")
            return

        if options['source']:
            sources = FlightSource.objects.filter(name__icontains=options['source'], is_active=True)
        else:
            sources = FlightSource.objects.filter(
                is_active=True,
                source_type__in=['web_public', 'web_private'],
            )

        if not sources.exists():
            self.stdout.write(self.style.WARNING('No se encontraron fuentes.'))
            return

        for source in sources:
            self.stdout.write(f"Scraping {source.name}...")
            scraper = get_scraper_for_source(source)
            if not scraper:
                self.stdout.write(self.style.WARNING(f"  No hay scraper para {source.name}"))
                continue

            try:
                results = scraper.scrape()
                self.stdout.write(self.style.SUCCESS(f"  {len(results)} resultados"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Error: {e}"))
