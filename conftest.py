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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")  # Драйвер передается через фикстуру
        if driver:
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
            if call.excinfo:  # Если во время теста произошло исключение
                allure.attach(str(call.excinfo), name="Exception Info", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """Снимает скриншот при падении теста и добавляет в отчёт Allure"""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        if driver:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_name = f"screenshot_{timestamp}.png"
            screenshot_path = os.path.join("allure-results", screenshot_name)

            os.makedirs("allure-results", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Ошибка - скриншот", attachment_type=allure.attachment_type.PNG)