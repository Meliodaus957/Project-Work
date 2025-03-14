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
def browser(request):
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


