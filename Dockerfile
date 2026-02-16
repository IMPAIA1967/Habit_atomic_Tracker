FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Создаём непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash app
USER app

# Порт, который будет слушать Django
EXPOSE 8000

# Запуск сервера разработки
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]