import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    """Добавление опций командной строки для pytest."""
    parser.addoption("--browser", action="store", default="chrome",
                     help="Choose browser: chrome, firefox")
    parser.addoption("--executor", action="store", default="localhost")
    parser.addoption("--bv")


@pytest.fixture()
def driver(request):
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

    yield browser

    browser.quit()


# Хук для снятия скриншота в случае неудачи теста
def pytest_runtest_makereport(item, call):
    """Обрабатывает отчёт о тесте и прикладывает скриншот, если тест не прошёл."""
    if call.when == "call" and call.excinfo is not None:
        # Получаем драйвер из фикстуры
        driver = item.funcargs.get('driver')

        if driver:
            # Делаем снимок экрана и сохраняем в директории screenshots
            screenshot_dir = 'screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_name = f"{item.nodeid.replace('::', '_')}_{int(time.time())}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)

            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved at {screenshot_path}")
