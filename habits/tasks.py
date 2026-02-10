import logging
from datetime import timezone

from celery import shared_task
from django.conf import settings
from habits.models import Habit
from telegram import Bot

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_notification(habit_id):
    """
    Отправляет уведомление о привычке в Telegram.
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        message = (
            f"Напоминание!\n"
            f"Время выполнить привычку:\n"
            f"**{habit.action}**\n"
            f"Место: {habit.place}\n"
            f"Длительность: {habit.duration} сек"
        )

        # Отправляем сообщение пользователю
        bot.send_message(chat_id=habit.user.telegram_chat_id, text=message, parse_mode="Markdown")
        logger.info(f"Уведомление отправлено пользователю {habit.user.id} о привычке {habit.id}")
    except Habit.DoesNotExist:
        logger.error(f"Habit с id={habit_id} не найдена")
    except Exception as e:
        logger.error(f"Ошибка при отправке Telegram-уведомления: {e}")

@shared_task
def send_habit_reminders():
    """
    Проверяет все привычки и отправляет уведомления тем,
    у кого время выполнения совпадает с текущим (с точностью до часа).
    """
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    current_hour = current_time.hour
    current_minute = current_time.minute

    # Находим привычки, у которых время выполнения совпадает с текущим часом
    habits = Habit.objects.filter(
        time__hour=current_hour,
        time__minute=current_minute
    )

    for habit in habits:
        send_telegram_notification.delay(habit.id)