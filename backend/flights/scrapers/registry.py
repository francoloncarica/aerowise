"""Registry de scrapers — mapea nombres de fuentes a clases de scraper."""
import logging

from .globeair import GlobeAirScraper
from .avconjet import AvconJetScraper
from .proair import ProAirScraper
from .gestair import GestairScraper
from .luxaviation import LuxaviationScraper
from .vacantseat import VacantSeatScraper
from .feelingair import FeelingAirScraper
from .jetspartners import JetsPartnersScraper
from .pacificocean import PacificOceanScraper

logger = logging.getLogger(__name__)

# Mapeo de nombre de fuente (lower) → clase scraper
SCRAPER_REGISTRY = {
    'globeair': GlobeAirScraper,
    'avcon jet': AvconJetScraper,
    'avconjet': AvconJetScraper,
    'proair': ProAirScraper,
    'gestair': GestairScraper,
    'luxaviation': LuxaviationScraper,
    'vacant seat': VacantSeatScraper,
    'vacantseat': VacantSeatScraper,
    'feeling air': FeelingAirScraper,
    'feelingair': FeelingAirScraper,
    'jets partners': JetsPartnersScraper,
    'jetspartners': JetsPartnersScraper,
    'pacific ocean': PacificOceanScraper,
    'pacificocean': PacificOceanScraper,
}


def get_scraper_for_source(source):
    """Retorna una instancia del scraper apropiado para la fuente, o None."""
    name_lower = source.name.lower().strip()

    # Buscar match exacto primero
    scraper_class = SCRAPER_REGISTRY.get(name_lower)

    if not scraper_class:
        # Buscar match parcial
        for key, cls in SCRAPER_REGISTRY.items():
            if key in name_lower or name_lower in key:
                scraper_class = cls
                break

    if scraper_class:
        return scraper_class(source)

    logger.warning(f"No hay scraper registrado para: {source.name}")
    return None
