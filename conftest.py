import allure
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime

def pytest_addoption(parser):
    """Добавление опций командной строки для pytest."""
    parser.addoption("--browser", action="store", default="chrome",
                     help="Choose browser: chrome, firefox")
    parser.addoption("--executor", action="store", default="selenoid")
    parser.addoption("--bv")


@pytest.fixture()
def driver(request, base_url):
    """Фикстура для инициализации веб-драйвера на основе аргументов."""
    browser_name = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--bv")

    executor_url = f"http://{executor}:4444/wd/hub"

    # Инициализация драйвера на основе выбора браузера
    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    caps = {
        "browserName": browser_name,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    for k, v in caps.items():
        options.set_capability(k, v)

    browser = webdriver.Remote(
        command_executor=executor_url,
        options=options
    )

    browser.maximize_window()
    browser.get(base_url)

    yield browser

    browser.quit()


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