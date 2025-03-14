from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
    ITEM_TITLE = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    CART_ITEM_COUNT = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    def get_inventory_items(self):
        return self.driver.find_elements(*self.INVENTORY_ITEMS)

    def go_to_cart(self):
        self.click(*self.CART_BUTTON)

    def add_item_to_cart(self, index):
        items = self.get_inventory_items()
        items[index].find_element(*self.ADD_TO_CART_BUTTON).click()

    def get_cart_item_count(self):
        try:
            return int(self.get_text(*self.CART_ITEM_COUNT))
        except ValueError:
            return 0

    def sort_items_by_price(self, option="low-to-high"):
        self.click(*self.SORT_DROPDOWN)
        self.click(By.XPATH, f"//*[text()='{option.capitalize()}']")
