# Базовый образ с Python и минимальными зависимостями
FROM python:3.11-slim

# Устанавливаем зависимости системы (для Selenium, Chrome и Allure)
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    wget \
    xvfb \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Allure (для отчетов)
RUN curl -fsSL https://github.com/allure-framework/allure2/releases/download/2.23.0/allure-2.23.0.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-2.23.0/bin/allure /usr/bin/allure

# Устанавливаем Chrome и ChromeDriver
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-keyring.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/google-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Создаем директорию для проекта
WORKDIR /tests

# Копируем файлы проекта (код тестов)
COPY . /tests/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем поддержку Chrome для Selenium
ENV PATH="/usr/local/bin:${PATH}"

# Запуск тестов при старте контейнера
ENTRYPOINT ["pytest", "--alluredir=allure-results", "-q"]
