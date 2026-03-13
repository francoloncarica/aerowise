"""VacantSeat empty legs scraper — vacantseat.com/empty-legs"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class VacantSeatScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # Multi-estrategia
            self._try_cards(soup, results)
            if not results:
                self._try_table(soup, results)
            if not results:
                self._try_patterns(soup, results)

            self.source.record_success()
            logger.info(f"VacantSeat: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"VacantSeat scraping error: {e}")

        return results

    def _try_cards(self, soup, results):
        cards = soup.select('.card, .empty-leg, .flight-item, [class*="leg"], article')
        for card in cards:
            self._extract(card, results)

    def _try_table(self, soup, results):
        for table in soup.find_all('table'):
            for row in table.find_all('tr')[1:]:
                self._extract(row, results)

    def _try_patterns(self, soup, results):
        text = soup.get_text(separator='\n')
        for match in re.finditer(
            r'([A-Z]{3,4})\s*[-–→>]+\s*([A-Z]{3,4})', text
        ):
            context_start = max(0, match.start() - 100)
            context_end = min(len(text), match.end() + 100)
            context = text[context_start:context_end]

            departure_date = self.parse_date_flexible(context)
            if not departure_date:
                continue

            origin_code = match.group(1)
            dest_code = match.group(2)
            price, _ = self.parse_price(context)

            data = {
                'external_id': f"vs-{departure_date}-{origin_code}-{dest_code}",
                'origin': self.resolve_airport(origin_code),
                'destination': self.resolve_airport(dest_code),
                'origin_raw': origin_code,
                'destination_raw': dest_code,
                'departure_date': departure_date,
                'price_usd': price,
                'operator': 'Vacant Seat',
                'url': self.source.url,
            }
            results.append(self.create_or_update_leg(data))

    def _extract(self, element, results):
        text = element.get_text(separator=' ', strip=True)
        if len(text) < 10:
            return

        route_match = re.search(r'([A-Z]{3,4})\s*[-–→>]+\s*([A-Z]{3,4})', text)
        if not route_match:
            # Intentar con ciudades
            city_match = re.search(r'(.+?)\s*[-–→>]+\s*(.+?)(?:\d|$)', text)
            if not city_match:
                return
            origin_raw = city_match.group(1).strip()[:50]
            dest_raw = city_match.group(2).strip()[:50]
            origin_code = origin_raw
            dest_code = dest_raw
        else:
            origin_code = route_match.group(1)
            dest_code = route_match.group(2)
            origin_raw = origin_code
            dest_raw = dest_code

        departure_date = self.parse_date_flexible(text)
        if not departure_date:
            return

        price, _ = self.parse_price(text)

        data = {
            'external_id': f"vs-{departure_date}-{origin_raw}-{dest_raw}",
            'origin': self.resolve_airport(origin_code),
            'destination': self.resolve_airport(dest_code),
            'origin_raw': origin_raw,
            'destination_raw': dest_raw,
            'departure_date': departure_date,
            'price_usd': price,
            'operator': 'Vacant Seat',
            'url': self.source.url,
        }
        results.append(self.create_or_update_leg(data))
