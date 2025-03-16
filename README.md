# Project-Work
QA Automation Project (UI & API)
Автоматизированное тестирование UI и API с использованием Selenium, Pytest, Allure и Docker.



📌 Содержание

📌 О проекте

⚙️ Технологии

🛠 Установка и запуск

🚀 Запуск тестов

📊 Генерация Allure-отчётов

🐳 Запуск в Docker

📂 Структура проекта

📝 Контакты



# 📌 О проекте
Этот проект включает в себя UI и API автотесты для следующих ресурсов:

Frontend (UI-тесты): https://www.saucedemo.com/

Backend (API-тесты): https://reqres.in/

✅ Используется PageObject для UI-тестов.
✅ Тесты запускаются в Jenkins.
✅ Подключён Allure для отчётности.
✅ Логи пишутся в файл с ротацией.



# ⚙️ Технологии
✅ Python 3.10+ – язык программирования

✅ Pytest – тестовый фреймворк

✅ Selenium – UI-автоматизация

✅ Requests – API-тестирование

✅ Allure – отчёты

✅ Logging – логирование

✅ Docker – контейнеризация

✅ Jenkins – CI/CD


# 🛠 Установка и запуск

1️⃣ Установите зависимости

pip install -r requirements.txt

2️⃣ Установите selenoid
 Mac / Linux / Windows

https://aerokube.com/selenoid/latest/

3️⃣ Запустите Selenoid и Jenkins в одной сети

docker-compose up -d 



# 🚀 Запуск тестов
Запуск всех тестов

pytest tests/


Запуск UI-тестов

pytest -m ui


Запуск API-тестов

pytest -m api


Запуск smoke-тестов

pytest -m smoke



# 📊 Генерация Allure-отчётов
1️⃣ Запустить тесты с сохранением отчёта:

pytest --alluredir=allure-results

2️⃣ Генерировать HTML-отчёт:

allure serve allure-results



# 🐳 Запуск в Docker

1️⃣ Сборка контейнера

docker build -t qa-autotests .

2️⃣ Запуск контейнера

docker run --rm qa-autotests



# 📂 Структура проекта

📦 qa-automation-project

 ┣ 📂 pages                # PageObject для UI-тестов

 ┃ ┣ 📜 base_page.py       # Базовый класс для страниц

 ┃ ┣ 📜 login_page.py      # Страница логина

 ┃ ┣ 📜 inventory_page.py  # Страница товаров

 ┃ ┗ 📜 cart_page.py       # Страница корзины

 ┣ 📂 tests                # Тесты

 ┃ ┣ 📜 test_ui.py         # UI-тесты

 ┃ ┣ 📜 test_api.py        # API-тесты

 ┃ ┗ 📜 conftest.py        # Фикстуры Pytest

 ┣ 📂 logs                 # Логи тестов (с ротацией)

 ┣ 📜 logger.py            # Настройки логирования

 ┣ 📜 requirements.txt     # Зависимости проекта

 ┣ 📜 pytest.ini           # Настройки Pytest

 ┣ 📜 Dockerfile           # Конфигурация Docker

 ┗ 📜 README.md            # Документация



# 📝 Контакты

👨‍💻 Автор: QA Automation Engineer

📧 Email: roman.temirgaleev@gmail.com

🚀 GitHub: Meliodaus957


