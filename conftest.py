import allure
import pytest
import os
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    # Настройка драйвера
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск браузера в фоновом режиме (без графического интерфейса)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Создание экземпляра драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Перед каждым тестом выполняется установка драйвера
    yield driver

    # После выполнения теста драйвер закрывается
    driver.quit()


