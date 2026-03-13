"""Luxaviation empty legs scraper — luxaviation.com/en/empty-legs"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class LuxaviationScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            soup = self.get_page()

            # Multi-estrategia: cards, tablas, y regex
            found = self._try_cards(soup, results)
            if not found:
                found = self._try_table(soup, results)
            if not found:
                self._try_regex(soup, results)

            self.source.record_success()
            logger.info(f"Luxaviation: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"Luxaviation scraping error: {e}")

        return results

    def _try_cards(self, soup, results):
        cards = soup.select('.empty-leg-card, .leg-card, .flight-card, [class*="empty"], [class*="leg"]')
        if not cards:
            return False

        for card in cards:
            try:
                self._extract_from_element(card, results)
            except Exception as e:
                logger.warning(f"Luxaviation card error: {e}")
        return len(results) > 0

    def _try_table(self, soup, results):
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                try:
                    self._extract_from_element(row, results)
                except Exception as e:
                    logger.warning(f"Luxaviation table row error: {e}")
        return len(results) > 0

    def _try_regex(self, soup, results):
        text = soup.get_text(separator='\n')
        # Buscar patrones de ruta con fecha
        patterns = re.finditer(
            r'([A-Z]{3,4})\s*[-–→>]+\s*([A-Z]{3,4})[\s\S]{0,100}?(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})',
            text
        )
        for match in patterns:
            try:
                origin_code = match.group(1)
                dest_code = match.group(2)
                date_str = match.group(3)

                departure_date = self.parse_date_flexible(date_str)
                if not departure_date:
                    continue

                context = match.group(0)
                price, _ = self.parse_price(context)
                origin = self.resolve_airport(origin_code)
                destination = self.resolve_airport(dest_code)

                data = {
                    'external_id': f"lux-{departure_date}-{origin_code}-{dest_code}",
                    'origin': origin,
                    'destination': destination,
                    'origin_raw': origin_code,
                    'destination_raw': dest_code,
                    'departure_date': departure_date,
                    'price_usd': price,
                    'operator': 'Luxaviation',
                    'url': self.source.url,
                }
                leg = self.create_or_update_leg(data)
                results.append(leg)
            except Exception as e:
                logger.warning(f"Luxaviation regex error: {e}")

    def _extract_from_element(self, element, results):
        text = element.get_text(separator=' ', strip=True)
        if len(text) < 10:
            return

        route_match = re.search(r'([A-Z]{3,4})\s*[-–→>]+\s*([A-Z]{3,4})', text)
        if not route_match:
            return

        origin_code = route_match.group(1)
        dest_code = route_match.group(2)

        departure_date = self.parse_date_flexible(text)
        if not departure_date:
            return

        price, _ = self.parse_price(text)
        origin = self.resolve_airport(origin_code)
        destination = self.resolve_airport(dest_code)

        data = {
            'external_id': f"lux-{departure_date}-{origin_code}-{dest_code}",
            'origin': origin,
            'destination': destination,
            'origin_raw': origin_code,
            'destination_raw': dest_code,
            'departure_date': departure_date,
            'price_usd': price,
            'operator': 'Luxaviation',
            'url': self.source.url,
        }
        leg = self.create_or_update_leg(data)
        results.append(leg)
