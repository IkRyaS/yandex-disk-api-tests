import pytest

from src.api.client import YandexDiskClient
from src.api.resources import YandexDiskResources
from src.config import YandexConfig
from src.utils.tools import generate_unique_suffix
from src.data.text_data import TextData


def pytest_configure(config):
    """Проверка наличия токена перед запуском тестов."""
    if not YandexConfig.AUTH_TOKEN:
        pytest.exit("Не задан токен доступа.")


@pytest.fixture()
def yandex_client() -> YandexDiskClient:
    """Клиент с валидным токеном из конфига."""
    return YandexDiskClient()


@pytest.fixture()
def yandex_client_no_auth() -> YandexDiskClient:
    """Клиент без токена — для проверки 401."""
    return YandexDiskClient(token="")


@pytest.fixture()
def yandex_resources() -> YandexDiskResources:
    """Клиент для работы с ресурсами (папки/файлы)."""
    return YandexDiskResources()


@pytest.fixture()
def cleanup_folder(yandex_resources):
    """Регистрирует путь для удаления после теста."""
    created_paths = []

    def _register(path: str) -> str:
        created_paths.append(path)
        return path

    yield _register

    for path in created_paths:
        yandex_resources.delete_resource(path, permanently=True)


@pytest.fixture()
def temp_folder(yandex_resources):
    """Создаёт тестовую папку перед тестом и удаляет её после (если ещё существует)."""
    folder_name = f"{TextData.FOLDER_AUTOTESTS}{generate_unique_suffix()}"
    folder_path = YandexConfig.get_test_folder_path(folder_name)

    response = yandex_resources.create_folder(folder_path)
    assert response.status_code == 201, f"Не удалось создать тестовую папку: {response.text}"

    yield folder_path

    yandex_resources.delete_resource(folder_path, permanently=True)


@pytest.fixture()
def temp_folder_in_trash(yandex_resources):
    """Создаёт папку, удаляет её в корзину (не навсегда) и возвращает
    оригинальный путь и путь в корзине.
    """
    folder_name = f"{TextData.FOLDER_AUTOTESTS}{generate_unique_suffix()}"
    original_path = YandexConfig.get_test_folder_path(folder_name)

    create_response = yandex_resources.create_folder(original_path)
    assert create_response.status_code == 201

    delete_response = yandex_resources.delete_resource(original_path, permanently=False)
    assert delete_response.status_code in (202, 204)

    trash_path = None
    trash_contents = yandex_resources.get_trash_contents()

    if trash_contents.status_code == 200:
        items = trash_contents.json().get("_embedded", {}).get("items", [])
        for item in items:
            if item.get("name") == folder_name:
                trash_path = item.get("path")
                break

    yield {"original_path": original_path, "trash_path": trash_path}

    if trash_path:
        yandex_resources.delete_resource(trash_path, permanently=True)
    yandex_resources.delete_resource(original_path, permanently=True)