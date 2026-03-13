"""Base scraper con utilidades compartidas."""
import re
import logging
from datetime import datetime, date
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from flights.models import Airport, EmptyLeg

logger = logging.getLogger(__name__)

# Tasa de conversión EUR→USD aproximada
EUR_TO_USD = 1.08


class BaseScraper:
    """Clase base para todos los scrapers de empty legs."""

    def __init__(self, source):
        self.source = source
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

    def scrape(self):
        """Método principal: ejecuta el scraping y retorna lista de empty legs creados/actualizados."""
        raise NotImplementedError

    def get_page(self, url=None, **kwargs):
        """Descarga una página y retorna BeautifulSoup."""
        url = url or self.source.url
        timeout = kwargs.pop('timeout', 30)
        response = self.session.get(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')

    def parse_date_flexible(self, text):
        """Parsea fechas en múltiples formatos."""
        if not text:
            return None
        text = text.strip()

        formats = [
            '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y',
            '%d-%m-%Y', '%d.%m.%Y',
            '%B %d, %Y', '%b %d, %Y',
            '%d %B %Y', '%d %b %Y',
            '%Y/%m/%d',
            '%d %B', '%d %b',
            '%B %d', '%b %d',
        ]

        for fmt in formats:
            try:
                parsed = datetime.strptime(text, fmt)
                # Si no tiene año, asumir el actual o siguiente
                if '%Y' not in fmt:
                    today = date.today()
                    parsed = parsed.replace(year=today.year)
                    if parsed.date() < today:
                        parsed = parsed.replace(year=today.year + 1)
                return parsed.date()
            except ValueError:
                continue

        # Intentar regex para "14 Mar" o "Mar 14"
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
            'ene': 1, 'abr': 4, 'ago': 8, 'dic': 12,
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'june': 6, 'july': 7, 'august': 8, 'september': 9,
            'october': 10, 'november': 11, 'december': 12,
        }

        match = re.search(r'(\d{1,2})\s+(\w+)', text, re.IGNORECASE)
        if match:
            day = int(match.group(1))
            month_str = match.group(2).lower()
            month = month_map.get(month_str)
            if month:
                today = date.today()
                try:
                    d = date(today.year, month, day)
                    if d < today:
                        d = date(today.year + 1, month, day)
                    return d
                except ValueError:
                    pass

        match = re.search(r'(\w+)\s+(\d{1,2})', text, re.IGNORECASE)
        if match:
            month_str = match.group(1).lower()
            day = int(match.group(2))
            month = month_map.get(month_str)
            if month:
                today = date.today()
                try:
                    d = date(today.year, month, day)
                    if d < today:
                        d = date(today.year + 1, month, day)
                    return d
                except ValueError:
                    pass

        logger.warning(f"No se pudo parsear la fecha: {text}")
        return None

    def resolve_airport(self, text):
        """Resuelve texto a un Airport. Intenta IATA, ICAO, ciudad."""
        if not text:
            return None
        text = text.strip()

        # "City (IATA)" pattern
        match = re.match(r'(.+?)\s*\((\w{3,4})\)', text)
        if match:
            code = match.group(2).upper()
            airport = Airport.objects.filter(iata=code).first() or Airport.objects.filter(icao=code).first()
            if airport:
                return airport

        # Código directo (3 o 4 caracteres)
        if len(text) <= 4 and text.isalpha():
            code = text.upper()
            if len(code) == 3:
                airport = Airport.objects.filter(iata=code).first()
                if airport:
                    return airport
            airport = Airport.objects.filter(icao=code).first()
            if airport:
                return airport

        # ICAO pattern "XXXX" dentro del texto
        match = re.search(r'\b([A-Z]{4})\b', text)
        if match:
            airport = Airport.objects.filter(icao=match.group(1)).first()
            if airport:
                return airport

        # Búsqueda por ciudad
        airport = Airport.objects.filter(city__iexact=text).first()
        if airport:
            return airport

        return None

    def parse_price(self, text):
        """Extrae precio numérico de texto como '$12,500' o '€8.900'."""
        if not text:
            return None, 'USD'
        text = str(text).strip()

        currency = 'USD'
        if '€' in text or 'EUR' in text.upper():
            currency = 'EUR'
        elif '£' in text or 'GBP' in text.upper():
            currency = 'GBP'

        # Extraer número
        cleaned = re.sub(r'[^\d.,]', '', text)
        if not cleaned:
            return None, currency

        # Manejar separadores de miles
        if ',' in cleaned and '.' in cleaned:
            if cleaned.index(',') < cleaned.index('.'):
                cleaned = cleaned.replace(',', '')
            else:
                cleaned = cleaned.replace('.', '').replace(',', '.')
        elif ',' in cleaned:
            parts = cleaned.split(',')
            if len(parts[-1]) == 2:
                cleaned = cleaned.replace(',', '.')
            else:
                cleaned = cleaned.replace(',', '')

        try:
            amount = Decimal(cleaned)
            if currency == 'EUR':
                amount = amount * Decimal(str(EUR_TO_USD))
            return amount, currency
        except Exception:
            return None, currency

    def create_or_update_leg(self, data):
        """Crea o actualiza un EmptyLeg a partir de datos del scraper."""
        external_id = data.get('external_id', '')

        if external_id:
            leg, created = EmptyLeg.objects.update_or_create(
                source=self.source,
                external_id=external_id,
                defaults=data
            )
        else:
            # Sin external_id, crear siempre (evitar duplicados por fecha+ruta)
            existing = EmptyLeg.objects.filter(
                source=self.source,
                origin_raw=data.get('origin_raw', ''),
                destination_raw=data.get('destination_raw', ''),
                departure_date=data.get('departure_date'),
            ).first()

            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.save()
                return existing
            else:
                leg = EmptyLeg.objects.create(source=self.source, **data)

        return leg
