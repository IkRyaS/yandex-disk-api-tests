from typing import Optional

import allure
import requests

from src.config import YandexConfig


class YandexDiskClient:
    """Базовый клиент для работы с Yandex Disk REST API."""

    def __init__(self, token: Optional[str] = None):
        """Инициализация клиента.

        Args:
            token: OAuth токен.
                   Если None — используется YandexConfig.AUTH_TOKEN.
                   Если пустая строка "" — без авторизации.
        """
        self.base_url = YandexConfig.BASE_URL

        if token is None:
            self.token = YandexConfig.AUTH_TOKEN
        else:
            self.token = token if token else None

        self.session = requests.Session()
        self._set_headers()

    def _set_headers(self):
        """Установка заголовков запроса."""
        headers = {"Accept": "application/json"}

        if self.token:
            headers["Authorization"] = f"OAuth {self.token}"

        self.session.headers.update(headers)

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Выполняет HTTP-запрос.

        Args:
            method: HTTP метод.
            endpoint: Путь к эндпоинту.
            **kwargs: Дополнительные параметры.

        Returns:
            Объект ответа requests.Response.
        """
        url = f"{self.base_url}{endpoint}"

        with allure.step(f"{method} {endpoint}"):
            response = self.session.request(method, url, **kwargs)
            allure.attach(str(response.status_code), "HTTP статус", allure.attachment_type.TEXT)

            if response.text:
                try:
                    allure.attach(str(response.json()), "Тело ответа", allure.attachment_type.JSON)
                except ValueError:
                    allure.attach(response.text[:500], "Тело ответа", allure.attachment_type.TEXT)

            return response

    def get_disk_info(self) -> requests.Response:
        """Получение информации о диске пользователя.

        Returns:
            Объект ответа.
        """
        return self._request("GET", "/")