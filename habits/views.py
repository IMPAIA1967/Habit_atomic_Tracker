from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пользователь видит только свои привычки + публичные
        return Habit.objects.filter(
            user=self.request.user
        ) | Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        # Автоматически устанавливаем пользователя
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='public')
    def public_habits(self, request):
        """Список публичных привычек"""
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

# Create your views here.
