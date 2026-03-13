"""JetsPartners empty legs scraper — jets.partners/empty-legs"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class JetsPartnersScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # Cards + tablas
            elements = soup.select('.card, .empty-leg, .flight-card, [class*="leg"], article')
            if not elements:
                for table in soup.find_all('table'):
                    elements.extend(table.find_all('tr')[1:])

            for el in elements:
                try:
                    text = el.get_text(separator=' ', strip=True)
                    if len(text) < 10:
                        continue

                    route_match = re.search(r'([A-Z]{3,4})\s*[-–→>]+\s*([A-Z]{3,4})', text)
                    if not route_match:
                        continue

                    origin_code = route_match.group(1)
                    dest_code = route_match.group(2)

                    departure_date = self.parse_date_flexible(text)
                    if not departure_date:
                        continue

                    price, _ = self.parse_price(text)

                    # Buscar aeronave
                    aircraft_raw = ''
                    aircraft_match = re.search(
                        r'(Citation|Challenger|Learjet|Phenom|Legacy|Global|Gulfstream|Falcon|Hawker|King Air)\s*\w*',
                        text, re.IGNORECASE
                    )
                    if aircraft_match:
                        aircraft_raw = aircraft_match.group(0).strip()

                    data = {
                        'external_id': f"jp-{departure_date}-{origin_code}-{dest_code}",
                        'origin': self.resolve_airport(origin_code),
                        'destination': self.resolve_airport(dest_code),
                        'origin_raw': origin_code,
                        'destination_raw': dest_code,
                        'departure_date': departure_date,
                        'price_usd': price,
                        'aircraft_raw': aircraft_raw,
                        'operator': 'Jets Partners',
                        'url': self.source.url,
                    }
                    results.append(self.create_or_update_leg(data))

                except Exception as e:
                    logger.warning(f"JetsPartners: Error procesando elemento: {e}")

            self.source.record_success()
            logger.info(f"JetsPartners: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"JetsPartners scraping error: {e}")

        return results
