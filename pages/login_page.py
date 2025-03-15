from selenium.webdriver.common.by import By
from .base_page import BasePage
from logger import logger


class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")

    def login(self, username, password):
        """Вход в систему с указанными учетными данными"""
        logger.info(f"Попытка входа в систему с логином: {username}")
        try:
            self.send_keys(*self.USERNAME_FIELD, username)
            self.send_keys(*self.PASSWORD_FIELD, password)
            self.click(*self.LOGIN_BUTTON)
            logger.info("Клик по кнопке входа выполнен успешно")
        except Exception as e:
            logger.error(f"Ошибка при вводе учетных данных: {e}")
            raise

    def get_error_message(self):
        """Получение сообщения об ошибке входа"""
        logger.info("Проверка наличия сообщения об ошибке входа")
        try:
            error_message = self.get_text(*self.ERROR_MESSAGE)
            logger.warning(f"Сообщение об ошибке: {error_message}")
            return error_message
        except Exception as e:
            logger.error(f"Ошибка при получении сообщения об ошибке: {e}")
            raise
