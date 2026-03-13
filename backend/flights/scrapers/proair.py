"""ProAir empty legs scraper — proair.de/empty-legs/"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class ProAirScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # ProAir usa tabla HTML: Departure date | Time | Routing (ICAO-ICAO) | Flight time | Aircraft
            tables = soup.find_all('table')

            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 4:
                        continue

                    try:
                        date_text = cells[0].get_text(strip=True)
                        time_text = cells[1].get_text(strip=True) if len(cells) > 1 else ''
                        routing = cells[2].get_text(strip=True) if len(cells) > 2 else ''
                        aircraft_raw = cells[-1].get_text(strip=True) if len(cells) > 3 else ''

                        departure_date = self.parse_date_flexible(date_text)
                        if not departure_date:
                            continue

                        # Routing: "ICAO-ICAO" o "ICAO - ICAO"
                        route_match = re.match(r'([A-Z]{4})\s*[-–]\s*([A-Z]{4})', routing)
                        if not route_match:
                            continue

                        origin_icao = route_match.group(1)
                        dest_icao = route_match.group(2)

                        origin = self.resolve_airport(origin_icao)
                        destination = self.resolve_airport(dest_icao)

                        # Parsear hora
                        departure_time = None
                        time_match = re.search(r'(\d{1,2}):(\d{2})', time_text)
                        if time_match:
                            from datetime import time
                            departure_time = time(int(time_match.group(1)), int(time_match.group(2)))

                        data = {
                            'external_id': f"proair-{date_text}-{routing}",
                            'origin': origin,
                            'destination': destination,
                            'origin_raw': origin_icao,
                            'destination_raw': dest_icao,
                            'departure_date': departure_date,
                            'departure_time': departure_time,
                            'aircraft_raw': aircraft_raw,
                            'operator': 'ProAir',
                            'url': self.source.url,
                        }
                        leg = self.create_or_update_leg(data)
                        results.append(leg)

                    except Exception as e:
                        logger.warning(f"ProAir: Error procesando fila: {e}")
                        continue

            self.source.record_success()
            logger.info(f"ProAir: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"ProAir scraping error: {e}")

        return results
