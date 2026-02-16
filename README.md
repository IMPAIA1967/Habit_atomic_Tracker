# Habit Atomic Tracker

Бэкенд для трекера полезных привычек по методике Джеймса Клира "Атомные привычки".

## Технологии
- Django
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Telegram Bot API

## Установка и запуск

Будет добавлено после реализации.

1. Убедитесь, что установлены **Docker** и **Docker Compose**
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-логин/Habit_atomic_Tracker.git
   cd Habit_atomic_Tracker
   ```
## Запуск проекта:

```env
docker compose up --build
 ```
Приложение будет доступно по адресу:
http://localhost:8000

### Без Docker (только для разработки)

1) Создайте виртуальное окружение и установите зависимости:
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
2) Запустите сервер и Celery (см. раздел «Запуск фоновых задач» ниже)

 ### Деплой
- Проект автоматически деплоится на удалённый сервер при пуше в ветку homework.
- Адрес сервера: http://62.84.115.183:8000
- Сервер: Ubuntu 24.04 LTS в Yandex Cloud
- CI/CD: GitHub Actions (тесты → сборка → деплой)

## Уведомления в Telegram

Проект поддерживает отправку напоминаний о привычках через Telegram-бота.

### Настройка

1. Создайте бота в Telegram через [@BotFather](https://t.me/BotFather)
2. Получите токен бота (пример: `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`)
3. Добавьте токен в `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_бота

4. Напишите боту /start, чтобы он мог писать вам первым

### Получение chat_id

1. Напишите боту любое сообщение
2. Откройте в браузере

 ```env
   https://api.telegram.org/botВАШ_ТОКЕН/getUpdates
 ```
3. Найдите в ответе `"chat": { "id": 123456789 }`

### Запуск фоновых задач
Для работы уведомлений необходимо запустить три процесса:

```env
# Терминал 1: Django сервер
python manage.py runserver

# Терминал 2: Celery worker
celery -A habit_tracker worker --loglevel=info --pool=solo

# Терминал 3: Celery beat (планировщик)
celery -A habit_tracker beat --loglevel=info
```