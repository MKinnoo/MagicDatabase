from dataclasses import dataclass
from config import DEFAULT_LANGUAGE


@dataclass
class Translation:
    """
    Représente une traduction récupérée depuis Scryfall.
    """

    language: str

    name: str

    oracle_text: str

    found: bool = True

    def to_dict(self) -> dict[str, str]:
        """
        Convertit la traduction en dictionnaire.
        """
        return {
            "name": self.name,
            "oracle_text": self.oracle_text
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Translation":
        """
        Construit une traduction à partir d'un dictionnaire.
        """
        return cls(
            language=DEFAULT_LANGUAGE,
            name=data["name"],
            oracle_text=data["oracle_text"],
            found=True
        )