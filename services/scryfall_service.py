import logging
import time

import requests

from config import (
    API_DELAY,
    DEFAULT_LANGUAGE,
    SCRYFALL_API_URL,
    USER_AGENT,
)
from models.translation import Translation

logger = logging.getLogger(__name__)

HEADERS: dict[str, str] = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
}


class ScryfallService:

    """
    Service chargé des appels à l'API Scryfall.
    """

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

        url = SCRYFALL_API_URL.format(
            set=(set_code or "").lower(),
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

            return Translation(

                language=DEFAULT_LANGUAGE,

                name=data.get(
                    "printed_name",
                    ""
                ),

                oracle_text=data.get(
                    "printed_text",
                    ""
                ),

                found=True
            )

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