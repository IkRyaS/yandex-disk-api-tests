import allure

from src.config import YandexConfig
from src.data.text_data import TextData
from src.utils.tools import generate_unique_suffix


@allure.epic("Yandex Disk API")
@allure.feature("Авторизация")
class TestYandexDiskAuth:
    """Тесты авторизации Yandex Disk API."""

    @allure.title("Авторизация с валидным токеном")
    @allure.tag("positive")
    @allure.tag("smoke")
    @allure.description("""
    Шаги:
    1. Отправить GET запрос по адресу v1/disk/ с валидным токеном

    Ожидаемые результаты:
    - код ответа: 200 OK
    - тело ответа содержит поля "total_space" и "used_space"
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_with_valid_token(self, yandex_client):
        """Авторизация с валидным токеном."""
        with allure.step("Отправка GET запроса к /v1/disk/"):
            response = yandex_client.get_disk_info()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка наличия полей total_space и used_space"):
            data = response.json()
            assert "total_space" in data
            assert "used_space" in data

    @allure.title("Авторизация без токена")
    @allure.tag("negative")
    @allure.tag("smoke")
    @allure.description("""
    Шаги:
    1. Отправить GET запрос по адресу v1/disk/ без передачи токена

    Ожидаемые результаты:
    - код ответа: 401 UNAUTHORIZED
    - тело ответа содержит поля "error", "description", "message"
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_without_token(self, yandex_client_no_auth):
        """Авторизация без токена."""
        with allure.step("Отправка GET запроса к /v1/disk/ без токена"):
            response = yandex_client_no_auth.get_disk_info()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 401

        with allure.step("Проверка наличия полей error, description, message"):
            data = response.json()
            assert "error" in data
            assert "description" in data
            assert "message" in data


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками")
class TestCreateFolder:
    """Тесты создания папок (метод PUT)."""

    @allure.title("Создание новой папки")
    @allure.tag("positive")
    @allure.tag("smoke")
    @allure.description("Создание папки на диске через API")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_folder(self, yandex_resources, cleanup_folder):
        """Создание новой папки."""
        folder_name = f"{TextData.FOLDER_TEST}{generate_unique_suffix()}"
        folder_path = YandexConfig.get_test_folder_path(folder_name)

        with allure.step(f"Создание папки {folder_path}"):
            create_response = yandex_resources.create_folder(folder_path)
            assert create_response.status_code == 201, "Папка не создана"

        cleanup_folder(folder_path)

        with allure.step(f"Проверка создания папки {folder_path}"):
            info_response = yandex_resources.get_resource_info(folder_path)
            assert info_response.status_code == 200, "Папка не найдена после создания"
            data = info_response.json()
            assert data["type"] == "dir", f"Ресурс {folder_path} не является папкой"

    @allure.title("Создание уже существующей папки")
    @allure.tag("negative")
    @allure.tag("regression")
    @allure.description("Попытка создать папку с существующим именем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_duplicate_folder(self, yandex_resources, temp_folder):
        """Создание дубликата папки."""
        with allure.step(f"Попытка создать папку {temp_folder} повторно"):
            response = yandex_resources.create_folder(temp_folder)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 409

        with allure.step("Проверка тела ответа"):
            data = response.json()
            assert "error" in data
            assert data["error"] == "DiskPathPointsToExistentDirectoryError"


@allure.epic("Yandex Disk API")
@allure.feature("Управление папками")
class TestDeleteFolder:
    """Тесты удаления папок (метод DELETE)."""

    @allure.title("Удаление папки в корзину")
    @allure.tag("positive")
    @allure.tag("smoke")
    @allure.description("Удаление папки в корзину (не навсегда)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_folder_to_trash(self, yandex_resources, temp_folder):
        """Удаление папки в корзину."""
        with allure.step("Удаление папки в корзину"):
            response = yandex_resources.delete_resource(temp_folder, permanently=False)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code in (202, 204)

        with allure.step("Проверка отсутствия папки по исходному пути"):
            info_response = yandex_resources.get_resource_info(temp_folder)
            assert info_response.status_code == 404

    @allure.title("Удаление несуществующей папки")
    @allure.tag("negative")
    @allure.tag("regression")
    @allure.description("Попытка удалить папку, которой нет на диске")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_nonexistent_folder(self, yandex_resources):
        """Удаление несуществующей папки."""
        folder_name = f"{TextData.FOLDER_NONEXISTENT}{generate_unique_suffix()}"
        path = YandexConfig.get_test_folder_path(folder_name)

        with allure.step(f"Попытка удаления несуществующей папки {path}"):
            response = yandex_resources.delete_resource(path)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

        with allure.step("Проверка тела ответа"):
            data = response.json()
            assert "error" in data


@allure.epic("Yandex Disk API")
@allure.feature("Восстановление из корзины")
class TestRestoreFolder:
    """Тесты восстановления папок (метод PUT)."""

    @allure.title("Восстановление папки из корзины")
    @allure.tag("positive")
    @allure.tag("smoke")
    @allure.description("Удаление папки в корзину и восстановление")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_restore_folder_from_trash(self, yandex_resources, temp_folder_in_trash):
        """Восстановление папки из корзины."""
        original_path = temp_folder_in_trash["original_path"]
        trash_path = temp_folder_in_trash["trash_path"]

        if not trash_path:
            raise AssertionError("Папка не найдена в корзине")

        with allure.step(f"Восстановление папки по пути {trash_path}"):
            response = yandex_resources.restore_from_trash(trash_path, overwrite=True)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code in (200, 201, 202)

        with allure.step("Проверка восстановления папки"):
            info_response = yandex_resources.get_resource_info(original_path)
            assert info_response.status_code == 200
            data = info_response.json()
            assert data["type"] == "dir"


@allure.epic("Yandex Disk API")
@allure.feature("Копирование и перемещение ресурсов")
class TestCopyFolder:
    """Тесты копирования папок (метод POST)."""

    @allure.title("Копирование папки")
    @allure.tag("positive")
    @allure.tag("smoke")
    @allure.description("""
    Шаги:
    1. Создать папку source_folder
    2. Скопировать папку в target_folder

    Ожидаемые результаты:
    - код ответа на копирование: 201 CREATED
    - папка появилась по новому пути
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_copy_folder(self, yandex_resources, cleanup_folder):
        """Копирование папки."""
        suffix = generate_unique_suffix()
        source_folder = cleanup_folder(
            YandexConfig.get_test_folder_path(f"{TextData.FOLDER_SOURCE}_{suffix}")
        )
        target_folder = cleanup_folder(
            YandexConfig.get_test_folder_path(f"{TextData.FOLDER_TARGET}_{suffix}")
        )

        with allure.step(f"Создание исходной папки {source_folder}"):
            create_response = yandex_resources.create_folder(source_folder)
            assert create_response.status_code == 201

        with allure.step(f"Копирование папки из {source_folder} в {target_folder}"):
            copy_response = yandex_resources.copy_resource(source_folder, target_folder)
            assert copy_response.status_code == 201

        with allure.step(f"Проверка появления копии {target_folder}"):
            check_response = yandex_resources.get_resource_info(target_folder)
            assert check_response.status_code == 200
            assert check_response.json()["type"] == "dir"

    @allure.title("Копирование несуществующей папки")
    @allure.tag("negative")
    @allure.tag("regression")
    @allure.description("Попытка скопировать несуществующую папку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_copy_nonexistent_folder(self, yandex_resources, cleanup_folder):
        """Копирование несуществующей папки."""
        suffix = generate_unique_suffix()
        nonexistent_folder = YandexConfig.get_test_folder_path(f"{TextData.FOLDER_NONEXISTENT}_{suffix}")
        target_folder = cleanup_folder(
            YandexConfig.get_test_folder_path(f"{TextData.FOLDER_TARGET}_{suffix}")
        )

        with allure.step("Создание целевой папки"):
            yandex_resources.create_folder(target_folder)

        with allure.step(f"Попытка копирования несуществующей папки {nonexistent_folder}"):
            response = yandex_resources.copy_resource(nonexistent_folder, target_folder)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404


@allure.epic("Yandex Disk API")
@allure.feature("Копирование и перемещение ресурсов")
class TestMoveFolder:
    """Тесты перемещения папок (метод POST)."""

    @allure.title("Перемещение папки")
    @allure.tag("positive")
    @allure.tag("smoke")
    @allure.description("""
    Шаги:
    1. Создать папку
    2. Переместить папку под новым именем

    Ожидаемые результаты:
    - код ответа: 201 CREATED
    - папки нет по старому пути (404)
    - папка есть по новому пути (200)
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_move_folder(self, yandex_resources, cleanup_folder):
        """Перемещение папки (POST /resources/move)."""
        suffix = generate_unique_suffix()
        source_folder = cleanup_folder(
            YandexConfig.get_test_folder_path(f"{TextData.FOLDER_TO_MOVE}_{suffix}")
        )
        target_folder = cleanup_folder(
            YandexConfig.get_test_folder_path(f"{TextData.FOLDER_MOVED}_{suffix}")
        )

        with allure.step(f"Создание исходной папки {source_folder}"):
            create_response = yandex_resources.create_folder(source_folder)
            assert create_response.status_code == 201

        with allure.step(f"Перемещение папки из {source_folder} в {target_folder}"):
            move_response = yandex_resources.move_resource(source_folder, target_folder)
            assert move_response.status_code == 201

        with allure.step("Проверка отсутствия папки по старому пути"):
            old_location = yandex_resources.get_resource_info(source_folder)
            assert old_location.status_code == 404

        with allure.step("Проверка наличия папки по новому пути"):
            new_location = yandex_resources.get_resource_info(target_folder)
            assert new_location.status_code == 200
            assert new_location.json()["type"] == "dir"