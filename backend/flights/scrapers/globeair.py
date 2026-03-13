"""GlobeAir empty legs scraper — globeair.com/empty-legs"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class GlobeAirScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # Buscar links a empty legs individuales
            links = soup.select('a[href*="fly.globeair.com/el/"], a[href*="/empty-leg"]')

            for link in links:
                try:
                    text = link.get_text(separator=' ', strip=True)
                    # Pattern: "City (IATA) → City (IATA)"
                    route_match = re.search(
                        r'(\w[\w\s]+?)\s*\((\w{3})\)\s*[→\-–>]+\s*(\w[\w\s]+?)\s*\((\w{3})\)',
                        text
                    )

                    if not route_match:
                        continue

                    origin_city = route_match.group(1).strip()
                    origin_code = route_match.group(2).upper()
                    dest_city = route_match.group(3).strip()
                    dest_code = route_match.group(4).upper()

                    # Buscar fecha y precio en el contexto
                    parent = link.parent or link
                    parent_text = parent.get_text(separator=' ', strip=True)

                    departure_date = self.parse_date_flexible(parent_text)
                    if not departure_date:
                        continue

                    price, currency = self.parse_price(parent_text)

                    origin = self.resolve_airport(origin_code)
                    destination = self.resolve_airport(dest_code)

                    data = {
                        'external_id': link.get('href', ''),
                        'origin': origin,
                        'destination': destination,
                        'origin_raw': f"{origin_city} ({origin_code})",
                        'destination_raw': f"{dest_city} ({dest_code})",
                        'departure_date': departure_date,
                        'price_usd': price,
                        'operator': 'GlobeAir',
                        'url': link.get('href', ''),
                    }
                    leg = self.create_or_update_leg(data)
                    results.append(leg)

                except Exception as e:
                    logger.warning(f"GlobeAir: Error procesando link: {e}")
                    continue

            self.source.record_success()
            logger.info(f"GlobeAir: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"GlobeAir scraping error: {e}")

        return results
