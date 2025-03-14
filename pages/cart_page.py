from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    def get_cart_items(self):
        # Получаем все элементы товара в корзине
        return self.driver.find_elements(By.CLASS_NAME, "cart_item")

    def get_item_names(self):
        # Получаем названия всех товаров в корзине (только названия, без дополнительной информации)
        items = self.get_cart_items()
        item_names = []
        for item in items:
            name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
            item_names.append(name_element.text)
        return item_names
