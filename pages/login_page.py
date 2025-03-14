from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")

    def login(self, username, password):
        self.send_keys(*self.USERNAME_FIELD, username)
        self.send_keys(*self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(*self.ERROR_MESSAGE)
