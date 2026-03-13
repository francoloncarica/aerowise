"""Gestair empty legs scraper — grupogestair.es (ASP.NET con CSRF)"""
import re
import logging
from .base import BaseScraper

logger = logging.getLogger(__name__)


class GestairScraper(BaseScraper):
    def scrape(self):
        results = []
        try:
            config = self.source.config or {}
            username = config.get('username', '')
            password = config.get('password', '')

            # Obtener página de login para CSRF token
            login_url = config.get('login_url', self.source.url)
            soup = self.get_page(login_url)

            # Buscar tokens ASP.NET
            viewstate = ''
            validation = ''
            vs_input = soup.find('input', {'name': '__VIEWSTATE'})
            vv_input = soup.find('input', {'name': '__EVENTVALIDATION'})
            if vs_input:
                viewstate = vs_input.get('value', '')
            if vv_input:
                validation = vv_input.get('value', '')

            # Login si hay credenciales
            if username and password:
                login_data = {
                    '__VIEWSTATE': viewstate,
                    '__EVENTVALIDATION': validation,
                    'ctl00$ContentPlaceHolder1$txtUser': username,
                    'ctl00$ContentPlaceHolder1$txtPassword': password,
                    'ctl00$ContentPlaceHolder1$btnLogin': 'Login',
                }
                self.session.post(login_url, data=login_data, timeout=30)

            # Obtener página de empty legs
            empty_legs_url = config.get('empty_legs_url', self.source.url)
            soup = self.get_page(empty_legs_url)

            # Buscar elementos de empty legs (tablas, divs, cards)
            # Gestair puede usar diferentes layouts
            entries = soup.select('.empty-leg, .flight-item, tr.leg-row, .card')
            if not entries:
                entries = soup.find_all('tr')

            for entry in entries:
                try:
                    text = entry.get_text(separator=' ', strip=True)
                    if len(text) < 10:
                        continue

                    # Buscar patrón de ruta
                    route_match = re.search(
                        r'([A-Z]{3,4})\s*[-–→>]\s*([A-Z]{3,4})', text
                    )
                    if not route_match:
                        continue

                    origin_code = route_match.group(1)
                    dest_code = route_match.group(2)

                    departure_date = self.parse_date_flexible(text)
                    if not departure_date:
                        continue

                    origin = self.resolve_airport(origin_code)
                    destination = self.resolve_airport(dest_code)
                    price, _ = self.parse_price(text)

                    data = {
                        'external_id': f"gestair-{departure_date}-{origin_code}-{dest_code}",
                        'origin': origin,
                        'destination': destination,
                        'origin_raw': origin_code,
                        'destination_raw': dest_code,
                        'departure_date': departure_date,
                        'price_usd': price,
                        'operator': 'Gestair',
                        'url': self.source.url,
                    }
                    leg = self.create_or_update_leg(data)
                    results.append(leg)

                except Exception as e:
                    logger.warning(f"Gestair: Error procesando entry: {e}")
                    continue

            self.source.record_success()
            logger.info(f"Gestair: {len(results)} empty legs encontrados")

        except Exception as e:
            self.source.record_error(str(e))
            logger.error(f"Gestair scraping error: {e}")

        return results
