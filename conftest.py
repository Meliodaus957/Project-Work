import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    # Настройка опций Chrome
    options = Options()
    options.add_argument("--headless")  # Запуск браузера в фоновом режиме
    options.add_argument("--no-sandbox")  # Убираем sandbox (для CI/CD)
    options.add_argument("--disable-dev-shm-usage")  # Отключение использования shared memory
    options.add_argument("--remote-debugging-port=9222")  # Для отладки, если нужно

    # Создание экземпляра драйвера
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),  # Устанавливаем драйвер с помощью WebDriverManager
        options=options
    )

    # Возвращаем драйвер для использования в тестах
    yield driver

    # Закрытие драйвера после выполнения теста
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