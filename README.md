# Telegram Secretary Bot

Бот-секретарь для Telegram на **aiogram** 3.x с поддержкой естественного языка, PostgreSQL, APScheduler и мультиязычностью.

## Структура проекта

```
.
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── main.py
├── handlers/
│   ├── __init__.py
│   ├── menu.py
│   └── tasks.py
├── scheduler/
│   ├── __init__.py
│   └── scheduler.py
├── db/
│   ├── __init__.py
│   └── database.py
├── utils/
│   ├── __init__.py
│   ├── lang.py
│   └── parser.py
└── locales/
    ├── en.json
    └── ru.json
```

## Установка и запуск

1. Склонировать репозиторий.
2. Скопировать шаблон `.env.example` в `.env` и заполнить:
   - `TOKEN` — токен Telegram‑бота
   - `DB_URL` — строка подключения к базе PostgreSQL
   - `DEFAULT_LANGUAGE` — код языка по умолчанию (например, `ru` или `en`)

   ```bash
   cp .env.example .env
   ```
3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустить бота:
   ```bash
   python main.py
   ```

## Docker

Сборка и запуск через Docker:
```bash
docker build -t telegram-secretary .
docker run -d --env-file .env --name secretary_bot telegram-secretary
```

## Деплой на Railway

1. Добавить плагин PostgreSQL в проект Railway.
2. Создать Reference Variable `DB_URL` из `Postgres.DATABASE_URL` в сервисе бота.
3. Добавить в Variables сервиса:
   - `TOKEN`
   - `DEFAULT_LANGUAGE`
4. Нажать Deploy.

