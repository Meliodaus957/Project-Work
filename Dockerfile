FROM python:3.13-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    netcat-traditional \
    && apt-get clean

# Создаем рабочую папку и копируем файлы
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем код 
COPY . /app

# Запускаем pytest
ENTRYPOINT ["pytest"]

# Команда, которая будет выполнена после того, как wait-for-it.sh завершит ожидание
CMD ["pytest", "-v", "tests/ui_test", "tests/api_test", "--browser=chrome", "--bv=latest", "--executor=localhost"]
