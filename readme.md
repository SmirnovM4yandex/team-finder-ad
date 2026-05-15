# Team Finder

Team Finder — веб-приложение для поиска команды и совместной работы над проектами.

## Функциональность

- регистрация и авторизация пользователей;
- авторизация по email;
- редактирование профиля пользователя;
- загрузка аватара;
- автоматическая генерация аватара при регистрации;
- создание и редактирование проектов;
- участие в проектах;
- добавление проектов в избранное;
- закрытие проектов;
- просмотр пользователей и проектов;
- фильтрация пользователей по взаимодействиям с проектами.

---

# Стек технологий

- Python 3
- Django
- PostgreSQL
- Docker
- HTML
- CSS
- JavaScript

---

# Структура проекта

```text
core/       - общие константы и валидаторы
projects/   - приложение проектов
users/      - приложение пользователей
media/      - пользовательские файлы
static/     - статические файлы
```

---

# Запуск проекта

## Требования

* Docker
* Docker Compose

---

# Настройка переменных окружения

Перед запуском необходимо создать файл `.env` в корне проекта.

Пример содержимого:

```env
DJANGO_DEBUG=True

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=your_secret_key

TASK_VERSION=1
```

---

# Сборка и запуск проекта

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

---

# Загрузка данных

```bash
docker compose exec app python manage.py loaddata fixtures/test_data.json
```

---

# Применение миграций

Если миграции не применились автоматически:

```bash
docker compose exec app python manage.py migrate
```

---

# Создание суперпользователя

```bash
docker compose exec app python manage.py createsuperuser
```

---

# Остановка контейнеров

```bash
docker compose down
```

Для удаления томов PostgreSQL:

```bash
docker compose down -v
```

---

# Административная панель

Административная панель доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

---
