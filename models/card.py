from dataclasses import dataclass


@dataclass
class Card:
    """
    Représente une carte de Base_Reference.
    """

    row: int

    card_id: str

    set_code: str

    collector_number: str

    name_en: str

    name_fr: str

    oracle_text_en: str

    oracle_text_fr: str