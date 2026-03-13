"""Pacific Ocean empty legs scraper — pacific-ocean.com.ar/empty-leg-flights/"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class PacificOceanScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # Lightweight scraper
            elements = soup.select('.card, .empty-leg, article, .post, .entry, tr')

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

                    data = {
                        'external_id': f"po-{departure_date}-{origin_code}-{dest_code}",
                        'origin': self.resolve_airport(origin_code),
                        'destination': self.resolve_airport(dest_code),
                        'origin_raw': origin_code,
                        'destination_raw': dest_code,
                        'departure_date': departure_date,
                        'price_usd': price,
                        'operator': 'Pacific Ocean',
                        'url': self.source.url,
                    }
                    results.append(self.create_or_update_leg(data))

                except Exception as e:
                    logger.warning(f"PacificOcean: Error: {e}")

            self.source.record_success()
            logger.info(f"PacificOcean: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"PacificOcean scraping error: {e}")

        return results
