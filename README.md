# Yandex Disk API Autotests

Автотесты для REST API Яндекс.Диска: https://yandex.ru/dev/disk/api/concepts/about-docpage/

## Стек
- Python 3.11+
- pytest
- requests
- allure-pytest
- uv

## Подготовка

### 1. Установка uv
```bash
pip install uv
```

### 2. Создание тестового аккаунта
1. Создайте отдельный тестовый Яндекс-аккаунт (не используйте личный)
2. Перейдите на полигон Яндекс.Диска: https://yandex.ru/dev/disk/poligon/
3. Получите OAuth-токен для тестового аккаунта

### 3. Настройка проекта
**Клонирование репозитория:**
```bash
git clone https://github.com/IkRyaS/yandex-disk-api-tests.git
cd yandex-disk-api-tests
```

**Создание файла .env в корне проекта с токеном:**
```bash
echo "YA_DISK_TOKEN=ваш_токен" > .env
```

**Установка зависимостей через uv:**
```bash
uv sync
```

## Запуск тестов
```bash
#Запуск всех тестов
pytest

#Запуск с подробным выводом
pytest -v

#С отчётом Allure
pytest --alluredir=allure-results

#Просмотр отчета
allure serve allure-results

#Запуск с Docker
docker-compose up tests
```

## Покрытие тестов
| HTTP метод | Тест | Тип |
|------------|------|-----|
| GET | Авторизация с валидным токеном | positive |
| GET | Авторизация без токена | negative |
| PUT | Создание новой папки | positive |
| PUT | Создание дубликата папки | negative |
| DELETE | Удаление папки в корзину | positive |
| DELETE | Удаление несуществующей папки | negative |
| PUT | Восстановление папки из корзины | positive |
| POST | Копирование папки | positive |
| POST | Копирование несуществующей папки | negative |
| POST | Перемещение папки | positive |
