from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)  # Пользователь устанавливается автоматически

    def validate(self, data):
        # Дополнительная валидация
        is_pleasant = data.get('is_pleasant', False)
        reward = data.get('reward', '')
        related_habit = data.get('related_habit')

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя указывать одновременно вознаграждение и связанную привычку."
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждение или связанную привычку."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        duration = data.get('duration')
        if duration and duration > 120:
            raise serializers.ValidationError(
                "Время на выполнение не должно превышать 120 секунд."
            )

        periodicity = data.get('periodicity')
        if periodicity and not (1 <= periodicity <= 7):
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        return data