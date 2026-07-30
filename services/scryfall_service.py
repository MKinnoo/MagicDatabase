import logging
import time

import requests

from config import (
    API_DELAY,
    DEFAULT_LANGUAGE,
    SCRYFALL_API_URL,
    USER_AGENT,
    CACHE_EXPIRATION_DAYS,
)
from datetime import (
    datetime,
    timedelta,
)
from models.cache_entry import CacheEntry
from models.translation import Translation
from repositories.cache_repository import CacheRepository

logger = logging.getLogger(__name__)

HEADERS: dict[str, str] = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
}


class ScryfallService:

    """
    Extrait la traduction d'une carte Scryfall.

    Gère les cartes simples ainsi que les cartes comportant plusieurs faces.
    """

    def __init__(self, cache_repository: CacheRepository):
        self._cache_repository = cache_repository

    def _extract_translation(
        self,
        card_data: dict
    ) -> Translation:
        """
        Extrait la traduction des cartes simples et recto-verso.
        """
        printed_name = card_data.get("printed_name")
        if printed_name:
            return Translation(
                language=DEFAULT_LANGUAGE,
                name=printed_name,
                oracle_text=card_data.get("printed_text", ""),
                found=True
            )

        faces = card_data.get("card_faces")
        card_names: list[str] = []
        card_oracle_parts: list[str] = []

        if faces:
            for face in faces:
                face_name = face.get("printed_name", "")
                face_text = face.get("printed_text", "")
                card_names.append(face_name)
                card_oracle_parts.append(
                    f"--- {face_name} ---\n\n"
                    f"{face_text}"
                )
            
            card_name = " // ".join(card_names)
            card_oracle = "\n\n".join(card_oracle_parts)
            return Translation(
                language=DEFAULT_LANGUAGE,
                name=card_name,
                oracle_text=card_oracle,
                found=True
            )

        return Translation(
            language=DEFAULT_LANGUAGE,
            name="",
            oracle_text="",
            found=True
        )

    def get_translation(
        self,
        set_code: str,
        collector_number: str
    ) -> Translation:

        """
        Récupère la traduction française d'une carte depuis l'API Scryfall.

        Args:
            set_code: Code de l'extension.
            collector_number: Numéro du collector.

        Returns:
            Une instance de Translation. Si la carte est introuvable ou
            qu'une erreur survient lors de l'appel à l'API, l'attribut
            found est positionné à False.
        """

        normalized_set_code = (set_code or "").lower()

        cache_key = f"{normalized_set_code}:{collector_number}"

        cache_entry = self._cache_repository.get(cache_key)

        if (
            cache_entry is not None
            and not self._is_cache_expired(cache_entry)
        ):

            logger.debug(
                "Cache hit pour %s",
                cache_key
            )

            return cache_entry.translation

        logger.debug(
            "Cache miss pour %s",
            cache_key
        )

        url = SCRYFALL_API_URL.format(
            set=normalized_set_code,
            collector=collector_number,
            language=DEFAULT_LANGUAGE
        )

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            time.sleep(API_DELAY)

            response.raise_for_status()

            data = response.json()

            translation = self._extract_translation(data)

            cache_entry = CacheEntry(
                translation=translation,
                updated_at=datetime.now()
            )

            self._cache_repository.put(
                cache_key,
                cache_entry
            )

            return translation

        except requests.RequestException as e:

            logger.error(
                "Erreur lors de l'appel à Scryfall (%s) : %s",
                url,
                e
            )

            return Translation(
                language=DEFAULT_LANGUAGE,
                name="",
                oracle_text="",
                found=False
            )

    def _is_cache_expired(
        self,
        cache_entry: CacheEntry
    ) -> bool:
        """
        Indique si une entrée du cache est expirée.
        """
        return (
            datetime.now() - cache_entry.updated_at
            > timedelta(days=CACHE_EXPIRATION_DAYS)
        )