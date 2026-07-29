from repositories.excel_repository import ExcelRepository
from services.scryfall_service import ScryfallService


class SyncService:

    """
    Synchronise Base_Reference.xlsx avec Scryfall.
    """

    def __init__(self):

        self.repository = ExcelRepository()

        self.scryfall = ScryfallService()

    def run(self):

        cards = self.repository.find_all()

        total = self.repository.count()

        success = 0

        failed = 0

        print()
        print("===== Synchronisation Scryfall =====")
        print()

        for index, card in enumerate(cards, start=1):

            print(
                f"[{index}/{total}] "
                f"{card.name_en}"
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

        print()

        print("Sauvegarde du fichier Excel...")

        self.repository.save()

        self.repository.close()

        print()

        print("===== Synchronisation terminée =====")

        print(f"Cartes mises à jour : {success}")

        print(f"Cartes introuvables : {failed}")