import os

from dotenv import load_dotenv

load_dotenv()


class YandexConfig:
    """Конфигурация для работы с Yandex Disk REST API."""

    BASE_URL = "https://cloud-api.yandex.net/v1/disk"
    AUTH_TOKEN = os.getenv("YA_DISK_TOKEN")

    @staticmethod
    def get_test_folder_path(name: str) -> str:
        """Возвращает путь к тестовому ресурсу.

        Args:
            name: Имя папки или файла.

        Returns:
            Путь в формате disk:/имя.
        """
        return f"disk:/{name}"
