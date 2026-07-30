from dataclasses import dataclass
from datetime import datetime

from models.translation import Translation


@dataclass(slots=True)
class CacheEntry:
    """
    Représente une entrée du cache Scryfall.
    """

    translation: Translation
    updated_at: datetime

    def to_dict(self) -> dict:
        """
        Convertit l'entrée du cache en dictionnaire.
        """
        return {
            "translation": self.translation.to_dict(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CacheEntry":
        """
        Construit une entrée du cache à partir d'un dictionnaire.
        """
        return cls(
            translation=Translation.from_dict(data["translation"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )