"""FeelingAir empty legs scraper — feelingair.com.ar"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class FeelingAirScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # Similar a VacantSeat
            cards = soup.select('.card, .empty-leg, .flight-item, [class*="leg"], article, .post, .entry')
            if not cards:
                cards = []
                for table in soup.find_all('table'):
                    cards.extend(table.find_all('tr')[1:])

            for card in cards:
                try:
                    text = card.get_text(separator=' ', strip=True)
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

                    data = {
                        'external_id': f"feeling-{departure_date}-{origin_code}-{dest_code}",
                        'origin': self.resolve_airport(origin_code),
                        'destination': self.resolve_airport(dest_code),
                        'origin_raw': origin_code,
                        'destination_raw': dest_code,
                        'departure_date': departure_date,
                        'price_usd': price,
                        'operator': 'Feeling Air',
                        'url': self.source.url,
                    }
                    results.append(self.create_or_update_leg(data))

                except Exception as e:
                    logger.warning(f"FeelingAir: Error procesando card: {e}")

            self.source.record_success()
            logger.info(f"FeelingAir: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"FeelingAir scraping error: {e}")

        return results
