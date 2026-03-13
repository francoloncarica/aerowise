"""Crea operadores y fuentes de datos iniciales."""
from django.core.management.base import BaseCommand
from flights.models import Operator, FlightSource


OPERATORS_AND_SOURCES = [
    {
        'operator': {
            'name': 'GlobeAir',
            'company_type': 'operator',
            'country': 'Austria',
            'city': 'Linz',
            'website': 'https://www.globeair.com',
            'description': 'Operador europeo de jets ligeros, líder en Citation Mustang.',
        },
        'source': {
            'name': 'GlobeAir',
            'source_type': 'web_public',
            'url': 'https://www.globeair.com/empty-legs',
            'description': 'Página pública de empty legs de GlobeAir',
            'scrape_interval_minutes': 60,
        },
    },
    {
        'operator': {
            'name': 'Avcon Jet',
            'company_type': 'operator',
            'country': 'Austria',
            'city': 'Vienna',
            'website': 'https://www.avconjet.at',
            'description': 'Operador premium de aviación ejecutiva con base en Vienna.',
        },
        'source': {
            'name': 'Avcon Jet',
            'source_type': 'web_public',
            'url': 'https://www.avconjet.at/en/empty-legs/',
            'description': 'Empty legs de Avcon Jet con mailto links',
            'scrape_interval_minutes': 120,
        },
    },
    {
        'operator': {
            'name': 'ProAir',
            'company_type': 'operator',
            'country': 'Alemania',
            'city': 'Munich',
            'website': 'https://www.proair.de',
            'description': 'Operador alemán de aviación ejecutiva.',
        },
        'source': {
            'name': 'ProAir',
            'source_type': 'web_public',
            'url': 'https://www.proair.de/empty-legs/',
            'description': 'Tabla HTML de empty legs de ProAir',
            'scrape_interval_minutes': 90,
        },
    },
    {
        'operator': {
            'name': 'Gestair',
            'company_type': 'operator',
            'country': 'España',
            'city': 'Madrid',
            'website': 'https://www.grupogestair.es',
            'description': 'Operador español de aviación privada.',
        },
        'source': {
            'name': 'Gestair',
            'source_type': 'web_private',
            'url': 'https://www.grupogestair.es/empty-legs',
            'description': 'Portal privado ASP.NET de Gestair (requiere login)',
            'scrape_interval_minutes': 120,
            'requires_auth': True,
            'config': {'login_url': 'https://www.grupogestair.es/login', 'username': '', 'password': ''},
        },
    },
    {
        'operator': {
            'name': 'Luxaviation',
            'company_type': 'operator',
            'country': 'Luxemburgo',
            'city': 'Luxembourg',
            'website': 'https://www.luxaviation.com',
            'description': 'Grupo global de aviación ejecutiva.',
        },
        'source': {
            'name': 'Luxaviation',
            'source_type': 'web_public',
            'url': 'https://www.luxaviation.com/en/empty-legs',
            'description': 'Página de empty legs de Luxaviation',
            'scrape_interval_minutes': 60,
        },
    },
    {
        'operator': {
            'name': 'Vacant Seat',
            'company_type': 'broker',
            'country': 'Reino Unido',
            'city': 'London',
            'website': 'https://www.vacantseat.com',
            'description': 'Broker británico de empty legs.',
        },
        'source': {
            'name': 'Vacant Seat',
            'source_type': 'web_public',
            'url': 'https://www.vacantseat.com/empty-legs',
            'description': 'Listado de empty legs de Vacant Seat',
            'scrape_interval_minutes': 60,
        },
    },
    {
        'operator': {
            'name': 'Feeling Air',
            'company_type': 'operator',
            'country': 'Argentina',
            'city': 'Buenos Aires',
            'website': 'https://www.feelingair.com.ar',
            'description': 'Operador argentino de aviación privada.',
        },
        'source': {
            'name': 'Feeling Air',
            'source_type': 'web_public',
            'url': 'https://www.feelingair.com.ar/empty-legs',
            'description': 'Empty legs de Feeling Air Argentina',
            'scrape_interval_minutes': 120,
        },
    },
    {
        'operator': {
            'name': 'Jets Partners',
            'company_type': 'broker',
            'country': 'Italia',
            'city': 'Milan',
            'website': 'https://jets.partners',
            'description': 'Broker europeo de jets privados.',
        },
        'source': {
            'name': 'Jets Partners',
            'source_type': 'web_public',
            'url': 'https://jets.partners/empty-legs',
            'description': 'Listado de empty legs de Jets Partners',
            'scrape_interval_minutes': 90,
        },
    },
    {
        'operator': {
            'name': 'Pacific Ocean',
            'company_type': 'operator',
            'country': 'Argentina',
            'city': 'Buenos Aires',
            'website': 'https://www.pacific-ocean.com.ar',
            'description': 'Operador argentino de vuelos privados.',
        },
        'source': {
            'name': 'Pacific Ocean',
            'source_type': 'web_public',
            'url': 'https://www.pacific-ocean.com.ar/empty-leg-flights/',
            'description': 'Empty legs de Pacific Ocean Argentina',
            'scrape_interval_minutes': 120,
        },
    },
    {
        'operator': {
            'name': 'Aeronáutica Florencio',
            'company_type': 'operator',
            'country': 'Argentina',
            'city': 'Buenos Aires',
            'website': '',
            'description': 'Operador argentino de aviación general.',
        },
        'source': {
            'name': 'Aeronáutica Florencio',
            'source_type': 'manual',
            'url': '',
            'description': 'Entrada manual de empty legs vía email/WhatsApp',
            'scrape_interval_minutes': 0,
        },
    },
    {
        'operator': {
            'name': 'Aerowise',
            'company_type': 'broker',
            'country': 'Argentina',
            'city': 'Buenos Aires',
            'website': '',
            'description': 'Broker Aerowise — entradas manuales propias.',
        },
        'source': {
            'name': 'Aerowise Manual',
            'source_type': 'manual',
            'url': '',
            'description': 'Empty legs ingresados manualmente por Aerowise',
            'scrape_interval_minutes': 0,
        },
    },
]


class Command(BaseCommand):
    help = 'Crea operadores y fuentes de datos iniciales'

    def handle(self, *args, **options):
        op_created = 0
        src_created = 0

        for item in OPERATORS_AND_SOURCES:
            op_data = item['operator']
            operator, created = Operator.objects.get_or_create(
                name=op_data['name'],
                defaults=op_data,
            )
            if created:
                op_created += 1

            src_data = item['source']
            requires_auth = src_data.pop('requires_auth', False)
            config = src_data.pop('config', {})
            source, created = FlightSource.objects.get_or_create(
                name=src_data['name'],
                defaults={
                    **src_data,
                    'operator': operator,
                    'requires_auth': requires_auth,
                    'config': config,
                },
            )
            if created:
                src_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Operadores: {op_created} creados. Fuentes: {src_created} creadas.'
        ))
