# Yandex Disk API Autotests

Автотесты для REST API Яндекс.Диска, написанные на Python + pytest.
Покрывают базовые сценарии работы с ресурсами (папками): создание, удаление,
восстановление из корзины, копирование, перемещение — включая позитивные и
негативные кейсы.

Документация API: https://yandex.ru/dev/disk/api/concepts/about-docpage/
Полигон для тестирования: https://yandex.ru/dev/disk/poligon/

## Стек

- Python 3.11+
- [pytest](https://github.com/pytest-dev/pytest) — тест-раннер
- [requests](https://github.com/psf/requests) — HTTP-клиент
- [allure-pytest](https://github.com/allure-framework/allure-python) — отчётность
- [uv](https://github.com/astral-sh/uv) — управление зависимостями и окружением
- Docker / docker-compose — опционально, для запуска без локальной установки Python

## Подготовка

### 1. Тестовый аккаунт и токен

Тесты создают, удаляют и модифицируют реальные ресурсы на Яндекс.Диске,
поэтому **не используйте личный аккаунт**.

1. Создайте отдельный тестовый Яндекс-аккаунт.
2. Перейдите на полигон: https://yandex.ru/dev/disk/poligon/
3. Получите OAuth-токен для этого аккаунта.

### 2. Клонирование репозитория

```bash
git clone https://github.com/IkRyaS/yandex-disk-api-tests.git
cd yandex-disk-api-tests
```

### 3. Файл с токеном

Создайте `.env` в корне проекта:

```bash
echo "YA_DISK_TOKEN=ваш_токен" > .env
```

Файл `.env` уже в `.gitignore` — токен не попадёт в репозиторий.

### 4. Установка зависимостей

**Вариант A — через uv (рекомендуется):**

```bash
pip install uv
uv sync
```

**Вариант B — через обычный venv + pip:**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Запуск тестов

С `uv`:

```bash
uv run pytest
```

Без `uv` (в активированном venv):

```bash
# Запуск всех тестов
pytest

# С подробным выводом
pytest -v

# С отчётом Allure
pytest --alluredir=allure-results

# Просмотр отчёта (нужен установленный Allure CLI)
allure serve allure-results
```

## Запуск в Docker

Токен подхватывается автоматически из `.env` в корне проекта — docker-compose
читает его сам, ничего дополнительно пробрасывать не нужно.

```bash
docker-compose up --build tests
```

Allure-результаты появятся в `./allure-results` на хосте (проброшено volume'ом).

## Покрытие тестов

| HTTP метод | Тест                              | Тип      |
|------------|------------------------------------|----------|
| GET        | Авторизация с валидным токеном     | positive |
| GET        | Авторизация без токена             | negative |
| PUT        | Создание новой папки               | positive |
| PUT        | Создание дубликата папки           | negative |
| PUT        | Восстановление папки из корзины    | positive |
| DELETE     | Удаление папки в корзину           | positive |
| DELETE     | Удаление несуществующей папки      | negative |
| POST       | Копирование папки                  | positive |
| POST       | Копирование несуществующей папки   | negative |
| POST       | Перемещение папки                  | positive |
