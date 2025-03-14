import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=allure.attachment_type.PNG)