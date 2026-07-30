"""
Configuration globale de l'application.
Equivalent du application.properties d'un projet Spring Boot.
"""

from pathlib import Path

# Dossier racine du projet
ROOT_DIRECTORY = Path(__file__).parent

# Excel
BASE_REFERENCE = ROOT_DIRECTORY / "Base_Reference.xlsx"
SHEET_NAME = "Cards"

# Cache
CACHE_DIRECTORY = ROOT_DIRECTORY / "cache"
CACHE_FILENAME = "scryfall_cache.json"

CACHE_PATH = CACHE_DIRECTORY / CACHE_FILENAME

CACHE_EXPIRATION_DAYS = 30

# Logs
LOG_DIRECTORY = ROOT_DIRECTORY / "logs"

# API
SCRYFALL_API_URL = "https://api.scryfall.com/cards/{set}/{collector}/{language}"

DEFAULT_LANGUAGE = "fr"

# Délai recommandé par Scryfall entre deux appels
API_DELAY = 0.1

APPLICATION_NAME = "MagicDatabase"
APPLICATION_VERSION = "1.0.0"

#USER_AGENT = f"{APPLICATION_NAME}/{APPLICATION_VERSION}"

USER_AGENT = (
    f"{APPLICATION_NAME}/{APPLICATION_VERSION} "
    "(https://github.com/MKinnoo/MagicDatabase)"
)