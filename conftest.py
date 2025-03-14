import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    # Автоматическая установка актуальной версии ChromeDriver
    options = webdriver.ChromeOptions()
    # Можно добавить параметры для Chrome (например, headless)
    options.add_argument("--headless")  # Опционально, если нужен headless режим

    # Использование WebDriverManager для загрузки и установки ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Возврат драйвера для использования в тестах
    yield driver

    # Очистка и закрытие браузера после завершения теста
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