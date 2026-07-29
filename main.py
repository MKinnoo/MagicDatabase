from logging_config import configure_logging
from services.sync_service import SyncService


def main() -> None:

    configure_logging()

    service = SyncService()

    service.run()


if __name__ == "__main__":
    main()