from dataclasses import dataclass


@dataclass
class Translation:
    """
    Représente une traduction récupérée depuis Scryfall.
    """

    language: str

    name: str

    oracle_text: str

    found: bool = True