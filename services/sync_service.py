import logging

from repositories.excel_repository import ExcelRepository
from services.scryfall_service import ScryfallService

logger = logging.getLogger(__name__)

class SyncService:

    """
    Synchronise Base_Reference.xlsx avec Scryfall.
    """


    def __init__(self) -> None:

        self.repository = ExcelRepository()

        self.scryfall = ScryfallService()

    def run(self) -> None:

        cards = self.repository.find_all()

        total = len(cards)

        success = 0

        failed = 0

        logger.info("-" * 60)
        logger.info("===== Synchronisation Scryfall =====")
        logger.info("-" * 60)

        for index, card in enumerate(cards, start=1):

            logger.info(
                "[%s/%s] %s",
                index,
                total,
                card.name_en
            )

            translation = self.scryfall.get_translation(

                card.set_code,

                card.collector_number

            )

            if translation.found:

                self.repository.update_translation(
                    card,
                    translation
                )

                success += 1

            else:

                failed += 1

        logger.info("-" * 60)

        logger.info("Sauvegarde du fichier Excel...")

        try:
            self.repository.save()
        finally:
            self.repository.close()

        logger.info("-" * 60)

        logger.info("===== Synchronisation terminée =====")

        logger.info("Cartes mises à jour : %s", success)
        
        logger.info("Cartes introuvables : %s", failed)