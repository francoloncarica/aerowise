"""AvconJet empty legs scraper — avconjet.at"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class AvconJetScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # AvconJet usa mailto links con subject "Empty Leg: Date Aircraft Route"
            mailto_links = soup.select('a[href^="mailto:"]')

            for link in mailto_links:
                try:
                    href = link.get('href', '')
                    if 'empty' not in href.lower() and 'leg' not in href.lower():
                        continue

                    # Extraer subject del mailto
                    subject_match = re.search(r'subject=([^&]+)', href)
                    if not subject_match:
                        continue

                    subject = subject_match.group(1).replace('%20', ' ').replace('+', ' ')

                    # Pattern: "Empty Leg: Date Aircraft Route"
                    # Ejemplo: "Empty Leg: 15.03.2026 Citation XLS Vienna - London"
                    parts_match = re.search(
                        r'Empty\s+Leg[:\s]+(.+?)\s+(\w[\w\s]+?)\s+(\w[\w\s]+?)\s*[-–→]\s*(\w[\w\s]+)',
                        subject, re.IGNORECASE
                    )

                    if not parts_match:
                        continue

                    date_str = parts_match.group(1).strip()
                    aircraft_raw = parts_match.group(2).strip()
                    origin_raw = parts_match.group(3).strip()
                    dest_raw = parts_match.group(4).strip()

                    departure_date = self.parse_date_flexible(date_str)
                    if not departure_date:
                        continue

                    origin = self.resolve_airport(origin_raw)
                    destination = self.resolve_airport(dest_raw)

                    # Buscar precio cerca del link
                    parent = link.find_parent(['div', 'tr', 'li']) or link.parent
                    price = None
                    if parent:
                        price_text = parent.get_text(separator=' ', strip=True)
                        price, _ = self.parse_price(price_text)

                    data = {
                        'external_id': f"avcon-{date_str}-{origin_raw}-{dest_raw}",
                        'origin': origin,
                        'destination': destination,
                        'origin_raw': origin_raw,
                        'destination_raw': dest_raw,
                        'departure_date': departure_date,
                        'aircraft_raw': aircraft_raw,
                        'price_usd': price,
                        'operator': 'Avcon Jet',
                        'url': self.source.url,
                    }
                    leg = self.create_or_update_leg(data)
                    results.append(leg)

                except Exception as e:
                    logger.warning(f"AvconJet: Error procesando mailto: {e}")
                    continue

            self.source.record_success()
            logger.info(f"AvconJet: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"AvconJet scraping error: {e}")

        return results
