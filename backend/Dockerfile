FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Команда запуска (использует PORT из переменных окружения или 8000 по умолчанию)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

