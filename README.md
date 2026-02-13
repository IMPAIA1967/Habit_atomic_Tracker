# Habit Atomic Tracker

Бэкенд для трекера полезных привычек по методике Джеймса Клира "Атомные привычки".

## Технологии
- Django
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Telegram Bot API

## Установка и запуск

Будет добавлено после реализации.
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



