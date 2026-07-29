from services.sync_service import SyncService


def main():

    service = SyncService()

    service.run()


if __name__ == "__main__":
    main()