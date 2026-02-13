import logging
import asyncio
from celery import shared_task
from django.conf import settings
from habits.models import Habit
from telegram import Bot

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_notification(habit_id):
    """
    Отправляет уведомление о привычке в Telegram (синхронная обёртка для асинхронного API).
    """
    logger.info(f"Запуск отправки уведомления для habit_id={habit_id}")
    try:
        habit = Habit.objects.get(id=habit_id)
        logger.info(f"Найдена привычка: {habit.action}, chat_id={habit.telegram_chat_id}")

        async def _send():
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            message = (
                f"Напоминание!\n"
                f"Время выполнить привычку:\n"
                f"**{habit.action}**\n"
                f"Место: {habit.place}\n"
                f"Длительность: {habit.duration} сек"
            )
            await bot.send_message(
                chat_id=habit.telegram_chat_id,
                text=message,
                parse_mode="Markdown"
            )

        # Запускаем асинхронную функцию из синхронного контекста
        asyncio.run(_send())
        logger.info(f"Уведомление отправлено пользователю {habit.user.id} о привычке {habit.id}")
    except Habit.DoesNotExist:
        logger.error(f"Habit с id={habit_id} не найдена")
    except Exception as e:
        logger.error(f"Ошибка при отправке Telegram-уведомления: {e}")


@shared_task
def send_habit_reminders():
    """
    Проверяет привычки по времени в часовом поясе Europe/Moscow.
    """
    from django.utils import timezone
    import pytz

    moscow_tz = pytz.timezone('Europe/Moscow')
    now_moscow = timezone.now().astimezone(moscow_tz)
    current_time = now_moscow.time()

    logger.info(f"Проверка привычек в Москве: {current_time.hour}:{current_time.minute}")

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    )

    logger.info(f"Найдено привычек: {habits.count()}")

    for habit in habits:
        logger.info(f"Отправка уведомления для привычки {habit.id}, chat_id={habit.telegram_chat_id}")
        send_telegram_notification.delay(habit.id)