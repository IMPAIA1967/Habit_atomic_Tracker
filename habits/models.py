from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Создатель привычки"
    )
    telegram_chat_id = models.BigIntegerField(
        verbose_name="Telegram Chat ID",
        help_text="ID чата для отправки уведомлений"
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место",
        help_text="Где выполнять привычку"
    )
    time = models.TimeField(
        verbose_name="Время",
        help_text="Когда выполнять привычку"
    )
    action = models.TextField(
        verbose_name="Действие",
        help_text="Что делать"
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Является ли привычка приятной (вознаграждением)"
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Только для полезных привычек; должна быть приятной"
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность (дней)",
        help_text="Как часто повторять (от 1 до 7 дней)"
    )
    reward = models.TextField(
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Чем вознаградить себя"
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение (сек)",
        help_text="Не более 120 секунд"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная",
        help_text="Доступна другим пользователям"
    )

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указывать одновременно вознаграждение и связанную привычку.")
        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")
        if self.duration > 120:
            raise ValidationError("Время на выполнение не должно превышать 120 секунд.")
        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user}: {self.action} в {self.place} в {self.time}"
