from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional
from logger import logger

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def wait_for_element(self, by: str, value: str, timeout: int = 10) -> WebElement:
        """Ожидание появления элемента на странице"""
        logger.info(f"Ожидание элемента {by}='{value}', таймаут: {timeout} сек")
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def click(self, by: str, value: str) -> None:
        """Клик по элементу"""
        logger.info(f"Попытка кликнуть по элементу {by}='{value}'")
        try:
            element = self.wait_for_element(by, value)
            element.click()
            logger.info(f"Клик выполнен: {by}='{value}'")
        except Exception as e:
            logger.error(f"Ошибка при клике на элемент {by}='{value}': {e}")
            raise

    def send_keys(self, by: str, value: str, text: str) -> None:
        """Ввод текста в поле"""
        logger.info(f"Ввод текста '{text}' в элемент {by}='{value}'")
        try:
            element = self.wait_for_element(by, value)
            element.clear()
            element.send_keys(text)
            logger.info(f"Текст введен в {by}='{value}'")
        except Exception as e:
            logger.error(f"Ошибка при вводе текста в элемент {by}='{value}': {e}")
            raise

    def get_text(self, by: str, value: str) -> str:
        """Получение текста из элемента"""
        logger.info(f"Получение текста из элемента {by}='{value}'")
        try:
            element = self.wait_for_element(by, value)
            text = element.text
            logger.info(f"Текст элемента {by}='{value}': '{text}'")
            return text
        except Exception as e:
            logger.error(f"Ошибка при получении текста из элемента {by}='{value}': {e}")
            raise

    def click_for_element(self, by: str, value: str, timeout: int = 10) -> Optional[WebElement]:
        """Ожидание кликабельности элемента"""
        logger.info(f"Ожидание кликабельности элемента {by}='{value}', таймаут: {timeout} сек")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            logger.info(f"Элемент {by}='{value}' стал кликабельным")
            return element
        except Exception as e:
            logger.error(f"Ошибка при ожидании кликабельности элемента {by}='{value}': {e}")
            raise
