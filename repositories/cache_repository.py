import json
import logging

from pathlib import Path

from models.cache_entry import CacheEntry

logger = logging.getLogger(__name__)


class CacheRepository:
    """
    Gère le cache local des traductions Scryfall.
    """

    def __init__(self, cache_path: Path):
        self._cache_path = cache_path

        self._cache_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize_cache_file()

        self._cache: dict[str, CacheEntry] = self._load_cache()

    def _initialize_cache_file(self) -> None:
        """
        Crée le fichier de cache s'il n'existe pas.
        """
        if not self._cache_path.exists():
            with self._cache_path.open("w", encoding="utf-8") as file:
                json.dump(
                    {},
                    file,
                    indent=4,
                    ensure_ascii=False
                )

    def _load_cache(self) -> dict[str, CacheEntry]:
        """
        Charge le cache en mémoire.
        """
        with self._cache_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            cache_key: CacheEntry.from_dict(entry_data)
            for cache_key, entry_data in data.items()
        }

    def get(self, cache_key: str) -> CacheEntry | None:
        """
        Retourne une entrée du cache.

        Args:
            cache_key: Clé de cache au format "<set>:<collector_number>".

        Returns:
            L'entrée du cache si elle existe, sinon None.
        """
        return self._cache.get(cache_key)

    def put(
        self,
        cache_key: str,
        cache_entry: CacheEntry
    ) -> None:
        """
        Ajoute ou met à jour une entrée du cache,
        puis sauvegarde le cache sur le disque.
        """
        self._cache[cache_key] = cache_entry

        self._save_cache()

    def _save_cache(self) -> None:
        """
        Sauvegarde le contenu du cache sur le disque.
        """
        with self._cache_path.open("w", encoding="utf-8") as file:
            json.dump(
                {
                    cache_key: entry.to_dict()
                    for cache_key, entry in self._cache.items()
                },
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.debug(
            "Cache Scryfall sauvegardé (%d cartes).",
            len(self._cache)
        )