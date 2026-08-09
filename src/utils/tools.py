import uuid

import allure


def generate_unique_suffix(length: int = 8) -> str:
    """Генерирует уникальный суффикс для тестовых данных.

    Args:
        length: Длина суффикса в символах.

    Returns:
        Уникальная строка из hex символов.
    """
    suffix = uuid.uuid4().hex[:length]
    allure.attach(suffix, "Сгенерированный суффикс", allure.attachment_type.TEXT)
    return suffix