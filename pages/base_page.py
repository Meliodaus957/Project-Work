from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def wait_for_element(self, by: str, value: str, timeout: int = 10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def click(self, by: str, value: str) -> None:
        element = self.wait_for_element(by, value)
        element.click()

    def send_keys(self, by: str, value: str, text: str) -> None:
        element = self.wait_for_element(by, value)
        element.send_keys(text)

    def get_text(self, by: str, value: str) -> str:
        element = self.wait_for_element(by, value)
        return element.text

    def click_for_element(self, by: str, value: str, timeout: int = 10) -> Optional[WebElement]:
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
