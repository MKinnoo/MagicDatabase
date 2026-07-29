import time

import requests


from config import API_DELAY
from config import DEFAULT_LANGUAGE
from config import SCRYFALL_API_URL
from config import USER_AGENT

from models.translation import Translation


class ScryfallService:

    """
    Service chargé des appels à l'API Scryfall.
    """

    def get_translation(
        self,
        set_code: str,
        collector_number: str
    ) -> Translation:

        url = SCRYFALL_API_URL.format(
            set=(set_code or "").lower(),
            collector=collector_number,
            language=DEFAULT_LANGUAGE
        )

        try:
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
                "Accept-Encoding": "gzip"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            time.sleep(API_DELAY)

            if response.status_code != 200:

                return Translation(
                    language=DEFAULT_LANGUAGE,
                    name="",
                    oracle_text="",
                    found=False
                )

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

        except Exception:

            return Translation(
                language=DEFAULT_LANGUAGE,
                name="",
                oracle_text="",
                found=False
            )