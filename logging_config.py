import logging

# TODO V1.1 : Ajouter un FileHandler pour enregistrer les logs dans logs/magic_database.log

def configure_logging() -> None:
    """
    Configure le système de journalisation de l'application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        force=True,
    )