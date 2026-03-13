"""Crea aeronaves de demostración en la base de datos."""
from django.core.management.base import BaseCommand
from flights.models import Aircraft


AIRCRAFT_DATA = [
    # Light Jets
    {'model': 'Citation Mustang', 'manufacturer': 'Cessna', 'category': 'light', 'max_passengers': 4, 'range_km': 2130, 'cruise_speed_kmh': 630},
    {'model': 'Citation CJ2', 'manufacturer': 'Cessna', 'category': 'light', 'max_passengers': 6, 'range_km': 2960, 'cruise_speed_kmh': 770},
    {'model': 'Citation CJ3', 'manufacturer': 'Cessna', 'category': 'light', 'max_passengers': 6, 'range_km': 3340, 'cruise_speed_kmh': 778},
    {'model': 'Citation CJ4', 'manufacturer': 'Cessna', 'category': 'light', 'max_passengers': 7, 'range_km': 3670, 'cruise_speed_kmh': 830},
    {'model': 'Phenom 100', 'manufacturer': 'Embraer', 'category': 'light', 'max_passengers': 4, 'range_km': 2182, 'cruise_speed_kmh': 720},
    {'model': 'Phenom 300', 'manufacturer': 'Embraer', 'category': 'light', 'max_passengers': 7, 'range_km': 3650, 'cruise_speed_kmh': 839},
    {'model': 'Learjet 40', 'manufacturer': 'Bombardier', 'category': 'light', 'max_passengers': 6, 'range_km': 3060, 'cruise_speed_kmh': 830},
    {'model': 'Learjet 45', 'manufacturer': 'Bombardier', 'category': 'light', 'max_passengers': 8, 'range_km': 3690, 'cruise_speed_kmh': 846},
    {'model': 'Learjet 60', 'manufacturer': 'Bombardier', 'category': 'light', 'max_passengers': 7, 'range_km': 4350, 'cruise_speed_kmh': 860},
    {'model': 'Learjet 75', 'manufacturer': 'Bombardier', 'category': 'light', 'max_passengers': 8, 'range_km': 3778, 'cruise_speed_kmh': 860},
    # Midsize Jets
    {'model': 'Citation XLS', 'manufacturer': 'Cessna', 'category': 'midsize', 'max_passengers': 8, 'range_km': 3440, 'cruise_speed_kmh': 795},
    {'model': 'Citation XLS+', 'manufacturer': 'Cessna', 'category': 'midsize', 'max_passengers': 8, 'range_km': 3500, 'cruise_speed_kmh': 800},
    {'model': 'Citation Sovereign', 'manufacturer': 'Cessna', 'category': 'midsize', 'max_passengers': 8, 'range_km': 5144, 'cruise_speed_kmh': 814},
    {'model': 'Hawker 800XP', 'manufacturer': 'Hawker Beechcraft', 'category': 'midsize', 'max_passengers': 8, 'range_km': 4600, 'cruise_speed_kmh': 828},
    {'model': 'Hawker 900XP', 'manufacturer': 'Hawker Beechcraft', 'category': 'midsize', 'max_passengers': 8, 'range_km': 5000, 'cruise_speed_kmh': 828},
    {'model': 'Gulfstream G280', 'manufacturer': 'Gulfstream', 'category': 'midsize', 'max_passengers': 10, 'range_km': 6667, 'cruise_speed_kmh': 850},
    # Super Midsize Jets
    {'model': 'Challenger 300', 'manufacturer': 'Bombardier', 'category': 'super_midsize', 'max_passengers': 10, 'range_km': 5741, 'cruise_speed_kmh': 870},
    {'model': 'Challenger 350', 'manufacturer': 'Bombardier', 'category': 'super_midsize', 'max_passengers': 10, 'range_km': 5926, 'cruise_speed_kmh': 870},
    {'model': 'Citation Latitude', 'manufacturer': 'Cessna', 'category': 'super_midsize', 'max_passengers': 9, 'range_km': 5278, 'cruise_speed_kmh': 828},
    # Heavy Jets
    {'model': 'Gulfstream G450', 'manufacturer': 'Gulfstream', 'category': 'heavy', 'max_passengers': 14, 'range_km': 8062, 'cruise_speed_kmh': 904},
    {'model': 'Gulfstream G550', 'manufacturer': 'Gulfstream', 'category': 'heavy', 'max_passengers': 16, 'range_km': 11390, 'cruise_speed_kmh': 904},
    {'model': 'Gulfstream G650', 'manufacturer': 'Gulfstream', 'category': 'heavy', 'max_passengers': 18, 'range_km': 12964, 'cruise_speed_kmh': 956},
    {'model': 'Global 6000', 'manufacturer': 'Bombardier', 'category': 'heavy', 'max_passengers': 14, 'range_km': 11112, 'cruise_speed_kmh': 904},
    {'model': 'Falcon 900LX', 'manufacturer': 'Dassault', 'category': 'heavy', 'max_passengers': 12, 'range_km': 8800, 'cruise_speed_kmh': 870},
    {'model': 'Falcon 7X', 'manufacturer': 'Dassault', 'category': 'heavy', 'max_passengers': 14, 'range_km': 11019, 'cruise_speed_kmh': 900},
    # Turboprops
    {'model': 'King Air 200', 'manufacturer': 'Beechcraft', 'category': 'turboprop', 'max_passengers': 6, 'range_km': 2980, 'cruise_speed_kmh': 536},
    {'model': 'King Air 350', 'manufacturer': 'Beechcraft', 'category': 'turboprop', 'max_passengers': 7, 'range_km': 3180, 'cruise_speed_kmh': 578},
    {'model': 'PC-12', 'manufacturer': 'Pilatus', 'category': 'turboprop', 'max_passengers': 6, 'range_km': 3417, 'cruise_speed_kmh': 528},
    {'model': 'PC-24', 'manufacturer': 'Pilatus', 'category': 'turboprop', 'max_passengers': 6, 'range_km': 3610, 'cruise_speed_kmh': 815},
]


class Command(BaseCommand):
    help = 'Crea aeronaves de demostración en la base de datos'

    def handle(self, *args, **options):
        created = 0
        existing = 0

        for data in AIRCRAFT_DATA:
            _, was_created = Aircraft.objects.get_or_create(
                model=data['model'],
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                existing += 1

        self.stdout.write(self.style.SUCCESS(
            f'Aeronaves: {created} creadas, {existing} ya existían. Total: {Aircraft.objects.count()}'
        ))
