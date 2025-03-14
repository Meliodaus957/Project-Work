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

    # Создание экземпляра драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Перед каждым тестом выполняется установка драйвера
    yield driver

    # После выполнения теста драйвер закрывается
    driver.quit()


