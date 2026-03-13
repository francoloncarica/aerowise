"""Crea consultas de demostración para los empty legs existentes."""
import random
from django.core.management.base import BaseCommand
from flights.models import EmptyLeg, Inquiry


DEMO_CONTACTS = [
    {'name': 'Carlos García', 'email': 'carlos.garcia@email.com', 'phone': '+54 11 4567-8901'},
    {'name': 'María López', 'email': 'maria.lopez@email.com', 'phone': '+54 11 5678-9012'},
    {'name': 'Juan Martínez', 'email': 'juan.martinez@email.com', 'phone': '+54 351 234-5678'},
    {'name': 'Ana Rodríguez', 'email': 'ana.rodriguez@email.com', 'phone': '+54 261 345-6789'},
    {'name': 'Roberto Fernández', 'email': 'roberto.f@email.com', 'phone': '+54 11 6789-0123'},
    {'name': 'Laura Sánchez', 'email': 'laura.sanchez@email.com', 'phone': '+1 305 555-0142'},
    {'name': 'James Wilson', 'email': 'j.wilson@email.com', 'phone': '+1 212 555-0198'},
    {'name': 'Sophie Martin', 'email': 'sophie.martin@email.com', 'phone': '+33 6 12 34 56 78'},
    {'name': 'Thomas Müller', 'email': 'thomas.muller@email.com', 'phone': '+49 171 234 5678'},
    {'name': 'Alessandro Rossi', 'email': 'a.rossi@email.com', 'phone': '+39 333 456 7890'},
]

DEMO_MESSAGES = [
    'Me interesa este vuelo, ¿tienen disponibilidad?',
    'Quisiera más información sobre este empty leg.',
    'Somos un grupo de {pax} personas, ¿podemos reservar?',
    '¿Cuál es el precio final con impuestos incluidos?',
    '¿Es posible cambiar la fecha un par de días?',
    'Estamos interesados. ¿Aceptan mascotas a bordo?',
    '¿Tienen catering disponible en este vuelo?',
    'Necesito confirmar para mañana, ¿está aún disponible?',
    '¿Hay opción de ida y vuelta?',
    'I am interested in this flight. Is it still available?',
]


class Command(BaseCommand):
    help = 'Crea consultas de demostración para empty legs existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=15,
            help='Cantidad de consultas a crear (default: 15)'
        )
        parser.add_argument('--clear', action='store_true', help='Elimina todas las consultas antes de crear')

    def handle(self, *args, **options):
        if options['clear']:
            deleted = Inquiry.objects.all().delete()[0]
            self.stdout.write(f'Eliminadas {deleted} consultas existentes')

        legs = list(EmptyLeg.objects.filter(status='available', published=True))
        if not legs:
            self.stdout.write(self.style.ERROR(
                'No hay empty legs disponibles y publicados. Ejecutá seed_demo_legs primero.'
            ))
            return

        count = min(options['count'], len(legs) * 2)
        created = 0
        statuses = ['pending', 'pending', 'pending', 'contacted', 'closed']

        for _ in range(count):
            leg = random.choice(legs)
            contact = random.choice(DEMO_CONTACTS)
            pax = random.randint(1, leg.max_passengers or 6)
            msg = random.choice(DEMO_MESSAGES).format(pax=pax)
            inquiry_status = random.choice(statuses)

            admin_notes = ''
            if inquiry_status == 'contacted':
                admin_notes = 'Cliente contactado por WhatsApp, esperando confirmación.'
            elif inquiry_status == 'closed':
                admin_notes = 'Reserva confirmada y pagada.'

            Inquiry.objects.create(
                empty_leg=leg,
                name=contact['name'],
                email=contact['email'],
                phone=contact['phone'],
                message=msg,
                passengers=pax,
                status=inquiry_status,
                admin_notes=admin_notes,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'{created} consultas de demo creadas. Total: {Inquiry.objects.count()}'
        ))
