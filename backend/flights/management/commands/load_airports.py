"""Carga 85+ aeropuertos hardcoded en la base de datos."""
from django.core.management.base import BaseCommand
from flights.models import Airport


AIRPORTS = [
    # Argentina
    {'icao': 'SAEZ', 'iata': 'EZE', 'name': 'Aeropuerto Internacional Ministro Pistarini', 'city': 'Buenos Aires', 'country': 'Argentina', 'latitude': -34.8222, 'longitude': -58.5358},
    {'icao': 'SABE', 'iata': 'AEP', 'name': 'Aeroparque Jorge Newbery', 'city': 'Buenos Aires', 'country': 'Argentina', 'latitude': -34.5592, 'longitude': -58.4156},
    {'icao': 'SAME', 'iata': 'MDZ', 'name': 'Aeropuerto Internacional El Plumerillo', 'city': 'Mendoza', 'country': 'Argentina', 'latitude': -32.8317, 'longitude': -68.7929},
    {'icao': 'SACO', 'iata': 'COR', 'name': 'Aeropuerto Internacional Ingeniero Ambrosio Taravella', 'city': 'Córdoba', 'country': 'Argentina', 'latitude': -31.3236, 'longitude': -64.2081},
    {'icao': 'SAAR', 'iata': 'ROS', 'name': 'Aeropuerto Internacional Islas Malvinas', 'city': 'Rosario', 'country': 'Argentina', 'latitude': -32.9036, 'longitude': -60.7850},
    {'icao': 'SAWH', 'iata': 'USH', 'name': 'Aeropuerto Internacional Malvinas Argentinas', 'city': 'Ushuaia', 'country': 'Argentina', 'latitude': -54.8431, 'longitude': -68.2956},
    {'icao': 'SAWC', 'iata': 'FTE', 'name': 'Aeropuerto Internacional Comandante Armando Tola', 'city': 'El Calafate', 'country': 'Argentina', 'latitude': -50.2803, 'longitude': -72.0531},
    {'icao': 'SASA', 'iata': 'SLA', 'name': 'Aeropuerto Internacional Martín Miguel de Güemes', 'city': 'Salta', 'country': 'Argentina', 'latitude': -24.8560, 'longitude': -65.4867},
    {'icao': 'SANC', 'iata': 'RCU', 'name': 'Aeropuerto de Río Cuarto', 'city': 'Río Cuarto', 'country': 'Argentina', 'latitude': -33.0861, 'longitude': -64.2614},
    {'icao': 'SAVC', 'iata': 'CRD', 'name': 'Aeropuerto General Enrique Mosconi', 'city': 'Comodoro Rivadavia', 'country': 'Argentina', 'latitude': -45.7853, 'longitude': -67.4656},
    {'icao': 'SANT', 'iata': 'TUC', 'name': 'Aeropuerto Internacional Teniente Benjamín Matienzo', 'city': 'Tucumán', 'country': 'Argentina', 'latitude': -26.8409, 'longitude': -65.1049},
    {'icao': 'SAVB', 'iata': 'BHI', 'name': 'Aeropuerto Comandante Espora', 'city': 'Bahía Blanca', 'country': 'Argentina', 'latitude': -38.7250, 'longitude': -62.1693},
    {'icao': 'SAAV', 'iata': 'SFN', 'name': 'Aeropuerto de Sauce Viejo', 'city': 'Santa Fe', 'country': 'Argentina', 'latitude': -31.7117, 'longitude': -60.8117},
    {'icao': 'SAZM', 'iata': 'MDQ', 'name': 'Aeropuerto Internacional Ástor Piazzolla', 'city': 'Mar del Plata', 'country': 'Argentina', 'latitude': -37.9342, 'longitude': -57.5733},
    {'icao': 'SAVT', 'iata': 'REL', 'name': 'Aeropuerto Almirante Marco Andrés Zar', 'city': 'Trelew', 'country': 'Argentina', 'latitude': -43.2106, 'longitude': -65.2703},
    # Uruguay
    {'icao': 'SUMU', 'iata': 'MVD', 'name': 'Aeropuerto Internacional de Carrasco', 'city': 'Montevideo', 'country': 'Uruguay', 'latitude': -34.8384, 'longitude': -56.0308},
    {'icao': 'SULS', 'iata': 'PDP', 'name': 'Aeropuerto Internacional Capitán de Corbeta Carlos A. Curbelo', 'city': 'Punta del Este', 'country': 'Uruguay', 'latitude': -34.8553, 'longitude': -55.0943},
    # Brasil
    {'icao': 'SBGR', 'iata': 'GRU', 'name': 'Aeroporto Internacional de São Paulo-Guarulhos', 'city': 'São Paulo', 'country': 'Brasil', 'latitude': -23.4356, 'longitude': -46.4731},
    {'icao': 'SBRJ', 'iata': 'SDU', 'name': 'Aeroporto Santos Dumont', 'city': 'Rio de Janeiro', 'country': 'Brasil', 'latitude': -22.9106, 'longitude': -43.1631},
    {'icao': 'SBGL', 'iata': 'GIG', 'name': 'Aeroporto Internacional do Galeão', 'city': 'Rio de Janeiro', 'country': 'Brasil', 'latitude': -22.8100, 'longitude': -43.2506},
    {'icao': 'SBBR', 'iata': 'BSB', 'name': 'Aeroporto Internacional de Brasília', 'city': 'Brasília', 'country': 'Brasil', 'latitude': -15.8711, 'longitude': -47.9186},
    {'icao': 'SBCF', 'iata': 'CNF', 'name': 'Aeroporto Internacional de Confins', 'city': 'Belo Horizonte', 'country': 'Brasil', 'latitude': -19.6244, 'longitude': -43.9719},
    {'icao': 'SBFL', 'iata': 'FLN', 'name': 'Aeroporto Internacional Hercílio Luz', 'city': 'Florianópolis', 'country': 'Brasil', 'latitude': -27.6703, 'longitude': -48.5525},
    # Chile
    {'icao': 'SCEL', 'iata': 'SCL', 'name': 'Aeropuerto Internacional Arturo Merino Benítez', 'city': 'Santiago', 'country': 'Chile', 'latitude': -33.3928, 'longitude': -70.7858},
    # USA
    {'icao': 'KJFK', 'iata': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'Estados Unidos', 'latitude': 40.6413, 'longitude': -73.7781},
    {'icao': 'KLGA', 'iata': 'LGA', 'name': 'LaGuardia Airport', 'city': 'New York', 'country': 'Estados Unidos', 'latitude': 40.7769, 'longitude': -73.8740},
    {'icao': 'KEWR', 'iata': 'EWR', 'name': 'Newark Liberty International Airport', 'city': 'Newark', 'country': 'Estados Unidos', 'latitude': 40.6925, 'longitude': -74.1687},
    {'icao': 'KTEB', 'iata': 'TEB', 'name': 'Teterboro Airport', 'city': 'Teterboro', 'country': 'Estados Unidos', 'latitude': 40.8501, 'longitude': -74.0608},
    {'icao': 'KMIA', 'iata': 'MIA', 'name': 'Miami International Airport', 'city': 'Miami', 'country': 'Estados Unidos', 'latitude': 25.7959, 'longitude': -80.2870},
    {'icao': 'KOPF', 'iata': 'OPF', 'name': 'Miami-Opa Locka Executive Airport', 'city': 'Miami', 'country': 'Estados Unidos', 'latitude': 25.9070, 'longitude': -80.2784},
    {'icao': 'KFLL', 'iata': 'FLL', 'name': 'Fort Lauderdale-Hollywood International Airport', 'city': 'Fort Lauderdale', 'country': 'Estados Unidos', 'latitude': 26.0726, 'longitude': -80.1527},
    {'icao': 'KLAX', 'iata': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'Estados Unidos', 'latitude': 33.9425, 'longitude': -118.4081},
    {'icao': 'KVNY', 'iata': 'VNY', 'name': 'Van Nuys Airport', 'city': 'Los Angeles', 'country': 'Estados Unidos', 'latitude': 34.2098, 'longitude': -118.4898},
    {'icao': 'KLAS', 'iata': 'LAS', 'name': 'Harry Reid International Airport', 'city': 'Las Vegas', 'country': 'Estados Unidos', 'latitude': 36.0840, 'longitude': -115.1537},
    {'icao': 'KORD', 'iata': 'ORD', 'name': "O'Hare International Airport", 'city': 'Chicago', 'country': 'Estados Unidos', 'latitude': 41.9742, 'longitude': -87.9073},
    {'icao': 'KATL', 'iata': 'ATL', 'name': 'Hartsfield-Jackson Atlanta International Airport', 'city': 'Atlanta', 'country': 'Estados Unidos', 'latitude': 33.6407, 'longitude': -84.4277},
    {'icao': 'KDAL', 'iata': 'DAL', 'name': 'Dallas Love Field', 'city': 'Dallas', 'country': 'Estados Unidos', 'latitude': 32.8471, 'longitude': -96.8518},
    {'icao': 'KHOU', 'iata': 'HOU', 'name': 'William P. Hobby Airport', 'city': 'Houston', 'country': 'Estados Unidos', 'latitude': 29.6454, 'longitude': -95.2789},
    {'icao': 'KASE', 'iata': 'ASE', 'name': 'Aspen-Pitkin County Airport', 'city': 'Aspen', 'country': 'Estados Unidos', 'latitude': 39.2232, 'longitude': -106.8688},
    # UK
    {'icao': 'EGLL', 'iata': 'LHR', 'name': 'London Heathrow Airport', 'city': 'London', 'country': 'Reino Unido', 'latitude': 51.4700, 'longitude': -0.4543},
    {'icao': 'EGGW', 'iata': 'LTN', 'name': 'London Luton Airport', 'city': 'London', 'country': 'Reino Unido', 'latitude': 51.8747, 'longitude': -0.3683},
    {'icao': 'EGLF', 'iata': 'FAB', 'name': 'Farnborough Airport', 'city': 'Farnborough', 'country': 'Reino Unido', 'latitude': 51.2758, 'longitude': -0.7763},
    {'icao': 'EGKB', 'iata': 'BQH', 'name': 'London Biggin Hill Airport', 'city': 'London', 'country': 'Reino Unido', 'latitude': 51.3308, 'longitude': 0.0325},
    {'icao': 'EGSS', 'iata': 'STN', 'name': 'London Stansted Airport', 'city': 'London', 'country': 'Reino Unido', 'latitude': 51.8850, 'longitude': 0.2350},
    # Francia
    {'icao': 'LFPB', 'iata': 'LBG', 'name': 'Aéroport de Paris-Le Bourget', 'city': 'Paris', 'country': 'Francia', 'latitude': 48.9694, 'longitude': 2.4414},
    {'icao': 'LFPG', 'iata': 'CDG', 'name': 'Aéroport Charles de Gaulle', 'city': 'Paris', 'country': 'Francia', 'latitude': 49.0097, 'longitude': 2.5479},
    {'icao': 'LFMN', 'iata': 'NCE', 'name': "Aéroport Nice Côte d'Azur", 'city': 'Nice', 'country': 'Francia', 'latitude': 43.6584, 'longitude': 7.2159},
    {'icao': 'LFML', 'iata': 'MRS', 'name': 'Aéroport de Marseille Provence', 'city': 'Marseille', 'country': 'Francia', 'latitude': 43.4393, 'longitude': 5.2214},
    # Alemania
    {'icao': 'EDDM', 'iata': 'MUC', 'name': 'Flughafen München', 'city': 'Munich', 'country': 'Alemania', 'latitude': 48.3538, 'longitude': 11.7861},
    {'icao': 'EDDF', 'iata': 'FRA', 'name': 'Frankfurt Airport', 'city': 'Frankfurt', 'country': 'Alemania', 'latitude': 50.0379, 'longitude': 8.5622},
    {'icao': 'EDDB', 'iata': 'BER', 'name': 'Berlin Brandenburg Airport', 'city': 'Berlin', 'country': 'Alemania', 'latitude': 52.3667, 'longitude': 13.5033},
    {'icao': 'EDDH', 'iata': 'HAM', 'name': 'Hamburg Airport', 'city': 'Hamburg', 'country': 'Alemania', 'latitude': 53.6304, 'longitude': 9.9882},
    # Austria
    {'icao': 'LOWW', 'iata': 'VIE', 'name': 'Vienna International Airport', 'city': 'Vienna', 'country': 'Austria', 'latitude': 48.1103, 'longitude': 16.5697},
    {'icao': 'LOWS', 'iata': 'SZG', 'name': 'Salzburg Airport', 'city': 'Salzburg', 'country': 'Austria', 'latitude': 47.7933, 'longitude': 13.0043},
    {'icao': 'LOWI', 'iata': 'INN', 'name': 'Innsbruck Airport', 'city': 'Innsbruck', 'country': 'Austria', 'latitude': 47.2602, 'longitude': 11.3439},
    # Suiza
    {'icao': 'LSGG', 'iata': 'GVA', 'name': 'Geneva Airport', 'city': 'Geneva', 'country': 'Suiza', 'latitude': 46.2381, 'longitude': 6.1089},
    {'icao': 'LSZH', 'iata': 'ZRH', 'name': 'Zürich Airport', 'city': 'Zürich', 'country': 'Suiza', 'latitude': 47.4647, 'longitude': 8.5492},
    # Italia
    {'icao': 'LIRF', 'iata': 'FCO', 'name': 'Aeroporto Internazionale Leonardo da Vinci', 'city': 'Roma', 'country': 'Italia', 'latitude': 41.8003, 'longitude': 12.2389},
    {'icao': 'LIMC', 'iata': 'MXP', 'name': 'Aeroporto di Milano-Malpensa', 'city': 'Milan', 'country': 'Italia', 'latitude': 45.6306, 'longitude': 8.7281},
    {'icao': 'LIPZ', 'iata': 'VCE', 'name': 'Aeroporto di Venezia Marco Polo', 'city': 'Venice', 'country': 'Italia', 'latitude': 45.5053, 'longitude': 12.3519},
    {'icao': 'LIRN', 'iata': 'NAP', 'name': 'Aeroporto di Napoli-Capodichino', 'city': 'Naples', 'country': 'Italia', 'latitude': 40.8860, 'longitude': 14.2908},
    # España
    {'icao': 'LEMD', 'iata': 'MAD', 'name': 'Aeropuerto Adolfo Suárez Madrid-Barajas', 'city': 'Madrid', 'country': 'España', 'latitude': 40.4983, 'longitude': -3.5676},
    {'icao': 'LEBL', 'iata': 'BCN', 'name': 'Aeropuerto Josep Tarradellas Barcelona-El Prat', 'city': 'Barcelona', 'country': 'España', 'latitude': 41.2971, 'longitude': 2.0785},
    {'icao': 'LEMG', 'iata': 'AGP', 'name': 'Aeropuerto de Málaga-Costa del Sol', 'city': 'Málaga', 'country': 'España', 'latitude': 36.6749, 'longitude': -4.4991},
    {'icao': 'LEPA', 'iata': 'PMI', 'name': 'Aeropuerto de Palma de Mallorca', 'city': 'Palma de Mallorca', 'country': 'España', 'latitude': 39.5517, 'longitude': 2.7388},
    {'icao': 'GCTS', 'iata': 'TFS', 'name': 'Aeropuerto de Tenerife Sur', 'city': 'Tenerife', 'country': 'España', 'latitude': 28.0445, 'longitude': -16.5725},
    {'icao': 'LEZL', 'iata': 'SVQ', 'name': 'Aeropuerto de Sevilla-San Pablo', 'city': 'Sevilla', 'country': 'España', 'latitude': 37.4180, 'longitude': -5.8932},
    # Portugal
    {'icao': 'LPPT', 'iata': 'LIS', 'name': 'Aeroporto Humberto Delgado', 'city': 'Lisboa', 'country': 'Portugal', 'latitude': 38.7756, 'longitude': -9.1354},
    {'icao': 'LPFR', 'iata': 'FAO', 'name': 'Aeroporto de Faro', 'city': 'Faro', 'country': 'Portugal', 'latitude': 37.0144, 'longitude': -7.9659},
    # Caribe
    {'icao': 'MDPC', 'iata': 'PUJ', 'name': 'Aeropuerto Internacional de Punta Cana', 'city': 'Punta Cana', 'country': 'República Dominicana', 'latitude': 18.5674, 'longitude': -68.3634},
    {'icao': 'MDSD', 'iata': 'SDQ', 'name': 'Aeropuerto Internacional Las Américas', 'city': 'Santo Domingo', 'country': 'República Dominicana', 'latitude': 18.4297, 'longitude': -69.6689},
    {'icao': 'MUVR', 'iata': 'VRA', 'name': 'Aeropuerto Internacional Juan Gualberto Gómez', 'city': 'Varadero', 'country': 'Cuba', 'latitude': 23.0344, 'longitude': -81.4353},
    {'icao': 'MUHA', 'iata': 'HAV', 'name': 'Aeropuerto Internacional José Martí', 'city': 'La Habana', 'country': 'Cuba', 'latitude': 22.9892, 'longitude': -82.4094},
    {'icao': 'MKJS', 'iata': 'MBJ', 'name': 'Sangster International Airport', 'city': 'Montego Bay', 'country': 'Jamaica', 'latitude': 18.5037, 'longitude': -77.9133},
    {'icao': 'TNCM', 'iata': 'SXM', 'name': 'Princess Juliana International Airport', 'city': 'Sint Maarten', 'country': 'Sint Maarten', 'latitude': 18.0410, 'longitude': -63.1089},
    {'icao': 'TNCA', 'iata': 'AUA', 'name': 'Queen Beatrix International Airport', 'city': 'Aruba', 'country': 'Aruba', 'latitude': 12.5014, 'longitude': -70.0152},
    # Mónaco / Grecia / Turquía
    {'icao': 'LFMD', 'iata': 'CEQ', 'name': 'Cannes-Mandelieu Airport', 'city': 'Cannes', 'country': 'Francia', 'latitude': 43.5420, 'longitude': 6.9535},
    {'icao': 'LGAV', 'iata': 'ATH', 'name': 'Athens International Airport', 'city': 'Athens', 'country': 'Grecia', 'latitude': 37.9364, 'longitude': 23.9445},
    {'icao': 'LGMK', 'iata': 'JMK', 'name': 'Mykonos Island National Airport', 'city': 'Mykonos', 'country': 'Grecia', 'latitude': 37.4351, 'longitude': 25.3481},
    {'icao': 'LTFM', 'iata': 'IST', 'name': 'Istanbul Airport', 'city': 'Istanbul', 'country': 'Turquía', 'latitude': 41.2608, 'longitude': 28.7419},
    {'icao': 'LTAI', 'iata': 'AYT', 'name': 'Antalya Airport', 'city': 'Antalya', 'country': 'Turquía', 'latitude': 36.8987, 'longitude': 30.8005},
    # Emiratos
    {'icao': 'OMDB', 'iata': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'Emiratos Árabes Unidos', 'latitude': 25.2528, 'longitude': 55.3644},
    # México
    {'icao': 'MMMX', 'iata': 'MEX', 'name': 'Aeropuerto Internacional Benito Juárez', 'city': 'Ciudad de México', 'country': 'México', 'latitude': 19.4363, 'longitude': -99.0721},
    {'icao': 'MMUN', 'iata': 'CUN', 'name': 'Aeropuerto Internacional de Cancún', 'city': 'Cancún', 'country': 'México', 'latitude': 21.0365, 'longitude': -86.8771},
    {'icao': 'MMSD', 'iata': 'SJD', 'name': 'Aeropuerto Internacional de Los Cabos', 'city': 'San José del Cabo', 'country': 'México', 'latitude': 23.1518, 'longitude': -109.7215},
]


class Command(BaseCommand):
    help = 'Carga 85+ aeropuertos en la base de datos'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for data in AIRPORTS:
            airport, created = Airport.objects.get_or_create(
                icao=data['icao'],
                defaults=data
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Aeropuertos: {created_count} creados, {updated_count} ya existían. Total: {Airport.objects.count()}'
        ))
