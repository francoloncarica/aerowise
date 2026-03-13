"""Crea 50 empty legs de demostración realistas."""
import random
from datetime import date, timedelta, time
from decimal import Decimal
from django.core.management.base import BaseCommand
from flights.models import Airport, FlightSource, EmptyLeg


DEMO_LEGS = [
    # --- Argentina doméstico ---
    {'origin': 'AEP', 'dest': 'MDZ', 'aircraft': 'Beechcraft King Air 350', 'price': 3200, 'original': 8500, 'pax': 7},
    {'origin': 'AEP', 'dest': 'COR', 'aircraft': 'Cessna Citation CJ3', 'price': 2800, 'original': 7200, 'pax': 6},
    {'origin': 'AEP', 'dest': 'USH', 'aircraft': 'Bombardier Challenger 300', 'price': 12000, 'original': 35000, 'pax': 10},
    {'origin': 'AEP', 'dest': 'SLA', 'aircraft': 'Pilatus PC-12', 'price': 2100, 'original': 5800, 'pax': 6},
    {'origin': 'AEP', 'dest': 'FTE', 'aircraft': 'Learjet 45', 'price': 11500, 'original': 32000, 'pax': 8},
    {'origin': 'AEP', 'dest': 'MDQ', 'aircraft': 'Beechcraft King Air 350', 'price': 2400, 'original': 6000, 'pax': 7},
    {'origin': 'AEP', 'dest': 'ROS', 'aircraft': 'Beechcraft King Air 200', 'price': 1800, 'original': 4500, 'pax': 6},
    {'origin': 'AEP', 'dest': 'TUC', 'aircraft': 'Pilatus PC-12', 'price': 2600, 'original': 7000, 'pax': 6},
    {'origin': 'COR', 'dest': 'MDZ', 'aircraft': 'Beechcraft King Air 200', 'price': 2200, 'original': 5500, 'pax': 6},
    {'origin': 'MDQ', 'dest': 'AEP', 'aircraft': 'Cessna Citation CJ2', 'price': 2000, 'original': 5200, 'pax': 6},
    # --- Argentina regional ---
    {'origin': 'EZE', 'dest': 'PUJ', 'aircraft': 'Learjet 45', 'price': 18500, 'original': 42000, 'pax': 8},
    {'origin': 'EZE', 'dest': 'GRU', 'aircraft': 'Cessna Citation XLS', 'price': 8500, 'original': 19000, 'pax': 8},
    {'origin': 'EZE', 'dest': 'MVD', 'aircraft': 'Learjet 40', 'price': 4200, 'original': 11000, 'pax': 6},
    {'origin': 'AEP', 'dest': 'PDP', 'aircraft': 'Beechcraft King Air 200', 'price': 3100, 'original': 8000, 'pax': 6},
    {'origin': 'EZE', 'dest': 'SCL', 'aircraft': 'Cessna Citation XLS+', 'price': 9000, 'original': 22000, 'pax': 8},
    {'origin': 'EZE', 'dest': 'SDU', 'aircraft': 'Learjet 75', 'price': 9500, 'original': 24000, 'pax': 8},
    {'origin': 'EZE', 'dest': 'GIG', 'aircraft': 'Gulfstream G280', 'price': 11000, 'original': 28000, 'pax': 10},
    {'origin': 'EZE', 'dest': 'BSB', 'aircraft': 'Bombardier Challenger 350', 'price': 14000, 'original': 36000, 'pax': 10},
    {'origin': 'EZE', 'dest': 'CUN', 'aircraft': 'Gulfstream G450', 'price': 28000, 'original': 65000, 'pax': 14},
    {'origin': 'GRU', 'dest': 'AEP', 'aircraft': 'Cessna Citation XLS', 'price': 7500, 'original': 18000, 'pax': 8},
    # --- Europa ---
    {'origin': 'VIE', 'dest': 'LTN', 'aircraft': 'Cessna Citation Mustang', 'price': 5400, 'original': 14000, 'pax': 4},
    {'origin': 'MUC', 'dest': 'PMI', 'aircraft': 'Cessna Citation CJ2', 'price': 4800, 'original': 12500, 'pax': 6},
    {'origin': 'MAD', 'dest': 'LIS', 'aircraft': 'Embraer Phenom 300', 'price': 5200, 'original': 13000, 'pax': 7},
    {'origin': 'LBG', 'dest': 'NCE', 'aircraft': 'Cessna Citation Mustang', 'price': 3500, 'original': 9000, 'pax': 4},
    {'origin': 'LBG', 'dest': 'GVA', 'aircraft': 'Cessna Citation XLS', 'price': 6200, 'original': 15000, 'pax': 8},
    {'origin': 'FRA', 'dest': 'VIE', 'aircraft': 'Cessna Citation CJ3', 'price': 4100, 'original': 10500, 'pax': 6},
    {'origin': 'FCO', 'dest': 'JMK', 'aircraft': 'Cessna Citation Sovereign', 'price': 7500, 'original': 18000, 'pax': 8},
    {'origin': 'BCN', 'dest': 'FAB', 'aircraft': 'Embraer Phenom 100', 'price': 4200, 'original': 10000, 'pax': 4},
    {'origin': 'MXP', 'dest': 'CDG', 'aircraft': 'Cessna Citation CJ3', 'price': 5000, 'original': 12000, 'pax': 6},
    {'origin': 'GVA', 'dest': 'SZG', 'aircraft': 'Pilatus PC-24', 'price': 3800, 'original': 9500, 'pax': 6},
    {'origin': 'LTN', 'dest': 'AGP', 'aircraft': 'Hawker 900XP', 'price': 7200, 'original': 19000, 'pax': 8},
    {'origin': 'IST', 'dest': 'DXB', 'aircraft': 'Bombardier Global 6000', 'price': 35000, 'original': 85000, 'pax': 14},
    {'origin': 'CDG', 'dest': 'BCN', 'aircraft': 'Cessna Citation CJ4', 'price': 4600, 'original': 11500, 'pax': 7},
    {'origin': 'MAD', 'dest': 'PMI', 'aircraft': 'Embraer Phenom 100', 'price': 3200, 'original': 8000, 'pax': 4},
    {'origin': 'VIE', 'dest': 'MUC', 'aircraft': 'Cessna Citation Mustang', 'price': 2800, 'original': 7500, 'pax': 4},
    {'origin': 'NCE', 'dest': 'FCO', 'aircraft': 'Cessna Citation CJ3', 'price': 4400, 'original': 11000, 'pax': 6},
    {'origin': 'LBG', 'dest': 'ATH', 'aircraft': 'Gulfstream G280', 'price': 12000, 'original': 30000, 'pax': 10},
    {'origin': 'FRA', 'dest': 'BER', 'aircraft': 'Cessna Citation Mustang', 'price': 3000, 'original': 7800, 'pax': 4},
    # --- USA ---
    {'origin': 'MIA', 'dest': 'PUJ', 'aircraft': 'Hawker 800XP', 'price': 9800, 'original': 25000, 'pax': 8},
    {'origin': 'TEB', 'dest': 'MIA', 'aircraft': 'Gulfstream G280', 'price': 15000, 'original': 38000, 'pax': 10},
    {'origin': 'VNY', 'dest': 'LAS', 'aircraft': 'Cessna Citation CJ4', 'price': 4500, 'original': 11000, 'pax': 7},
    {'origin': 'TEB', 'dest': 'ASE', 'aircraft': 'Bombardier Challenger 350', 'price': 18000, 'original': 45000, 'pax': 10},
    {'origin': 'OPF', 'dest': 'SXM', 'aircraft': 'Learjet 60', 'price': 11000, 'original': 28000, 'pax': 7},
    {'origin': 'JFK', 'dest': 'CUN', 'aircraft': 'Gulfstream G450', 'price': 22000, 'original': 52000, 'pax': 14},
    {'origin': 'LAX', 'dest': 'SJD', 'aircraft': 'Hawker 800XP', 'price': 8500, 'original': 21000, 'pax': 8},
    {'origin': 'MIA', 'dest': 'AUA', 'aircraft': 'Learjet 60', 'price': 10500, 'original': 26000, 'pax': 7},
    {'origin': 'ORD', 'dest': 'TEB', 'aircraft': 'Cessna Citation XLS+', 'price': 9000, 'original': 22000, 'pax': 8},
    {'origin': 'DAL', 'dest': 'MIA', 'aircraft': 'Bombardier Challenger 300', 'price': 14000, 'original': 35000, 'pax': 10},
    {'origin': 'ATL', 'dest': 'MBJ', 'aircraft': 'Hawker 900XP', 'price': 12000, 'original': 30000, 'pax': 8},
    {'origin': 'HOU', 'dest': 'CUN', 'aircraft': 'Gulfstream G280', 'price': 13500, 'original': 32000, 'pax': 10},
]


class Command(BaseCommand):
    help = 'Crea 50 empty legs de demostración realistas'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Elimina todos los empty legs antes de crear')

    def handle(self, *args, **options):
        if options['clear']:
            deleted = EmptyLeg.objects.all().delete()[0]
            self.stdout.write(f'Eliminados {deleted} empty legs existentes')

        # Obtener fuentes disponibles
        sources = list(FlightSource.objects.all())
        if not sources:
            self.stdout.write(self.style.ERROR('No hay fuentes. Ejecutá seed_sources primero.'))
            return

        today = date.today()
        created = 0

        for i, leg_data in enumerate(DEMO_LEGS):
            origin = Airport.objects.filter(iata=leg_data['origin']).first()
            dest = Airport.objects.filter(iata=leg_data['dest']).first()

            if not origin or not dest:
                self.stdout.write(self.style.WARNING(
                    f"Saltando {leg_data['origin']}→{leg_data['dest']}: aeropuerto no encontrado"
                ))
                continue

            # Fecha entre 1 y 21 días al futuro
            days_ahead = random.randint(1, 21)
            dep_date = today + timedelta(days=days_ahead)

            # Hora aleatoria entre 6:00 y 20:00
            dep_time = time(random.randint(6, 20), random.choice([0, 15, 30, 45]))

            source = random.choice(sources)
            price = Decimal(str(leg_data['price']))
            original = Decimal(str(leg_data['original']))

            origin_display = f"{origin.city} ({origin.iata})"
            dest_display = f"{dest.city} ({dest.iata})"

            EmptyLeg.objects.create(
                source=source,
                external_id=f"demo-{i+1}",
                origin=origin,
                destination=dest,
                origin_raw=origin_display,
                destination_raw=dest_display,
                departure_date=dep_date,
                departure_time=dep_time,
                aircraft_raw=leg_data['aircraft'],
                max_passengers=leg_data['pax'],
                price_usd=price,
                original_price_usd=original,
                operator=source.operator.name if source.operator else 'Aerowise',
                operator_company=source.operator,
                verified=True,
                published=True,
                status='available',
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'{created} empty legs de demo creados. Total: {EmptyLeg.objects.count()}'
        ))
