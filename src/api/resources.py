import allure
import requests

from .client import YandexDiskClient


class YandexDiskResources(YandexDiskClient):
    """Клиент для работы с ресурсами Yandex Disk (папки, файлы)."""

    def create_folder(self, path: str) -> requests.Response:
        """Создание папки на диске.

        Args:
            path: Путь к папке.

        Returns:
            Объект ответа.
        """
        with allure.step(f"Создание папки {path}"):
            params = {"path": path}
            return self._request("PUT", "/resources", params=params)

    def delete_resource(self, path: str, permanently: bool = False) -> requests.Response:
        """Удаление файла или папки.

        Args:
            path: Путь к ресурсу.
            permanently: Удалить навсегда (True) или в корзину (False).

        Returns:
            Объект ответа.
        """
        with allure.step(f"Удаление ресурса {path}"):
            params = {"path": path}
            if permanently:
                params["permanently"] = "true"
            return self._request("DELETE", "/resources", params=params)

    def restore_from_trash(self, path: str, overwrite: bool = True) -> requests.Response:
        """Восстановление ресурса из корзины.

        Args:
            path: Путь в корзине (например, "trash:/trash_folder_xxx").
            overwrite: Перезаписать существующий.

        Returns:
            Объект ответа.
        """
        with allure.step(f"Восстановление {path} из корзины"):
            params = {"path": path}
            if overwrite:
                params["overwrite"] = "true"
            return self._request("PUT", "/trash/resources/restore", params=params)

    def get_trash_contents(self) -> requests.Response:
        """Получение содержимого корзины.

        Returns:
            Объект ответа.
        """
        with allure.step("Получение содержимого корзины"):
            return self._request("GET", "/trash/resources")

    def get_resource_info(self, path: str) -> requests.Response:
        """Получение информации о ресурсе.

        Args:
            path: Путь к ресурсу.

        Returns:
            Объект ответа.
        """
        with allure.step(f"Получение информации о {path}"):
            params = {"path": path}
            return self._request("GET", "/resources", params=params)

    def copy_resource(self, from_path: str, to_path: str, overwrite: bool = False) -> requests.Response:
        """Копирование файла или папки (POST /resources/copy).

        Args:
            from_path: Путь к исходному ресурсу.
            to_path: Путь назначения.
            overwrite: Перезаписать, если ресурс по to_path уже существует.

        Returns:
            Объект ответа.
        """
        with allure.step(f"Копирование {from_path} -> {to_path}"):
            params = {
                "from": from_path,
                "path": to_path,
                "overwrite": "true" if overwrite else "false",
            }
            return self._request("POST", "/resources/copy", params=params)

    def move_resource(self, from_path: str, to_path: str, overwrite: bool = False) -> requests.Response:
        """Перемещение файла или папки (POST /resources/move).

        Args:
            from_path: Путь к исходному ресурсу.
            to_path: Путь назначения.
            overwrite: Перезаписать, если ресурс по to_path уже существует.

        Returns:
            Объект ответа.
        """
        with allure.step(f"Перемещение {from_path} -> {to_path}"):
            params = {
                "from": from_path,
                "path": to_path,
                "overwrite": "true" if overwrite else "false",
            }
            return self._request("POST", "/resources/move", params=params)
