# Базовый образ
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Копируем всё в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем CLI как точку входа
CMD ["python", "-m", "app.cli"]
