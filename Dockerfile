FROM python:3.14-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY main.py .
COPY openrouters.py .
COPY user_db.py .
COPY prompts.json .
COPY messages.json .

# Создаем директорию для базы данных и логов
RUN mkdir -p /data

# Запускаем бота
CMD ["python", "-u", "main.py"]

