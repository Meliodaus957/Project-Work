from selenium.webdriver.common.by import By
from .base_page import BasePage
from logger import logger


class InventoryPage(BasePage):
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
    ITEM_TITLE = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    CART_ITEM_COUNT = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    def get_inventory_items(self):
        """Получаем все товары на странице"""
        logger.info("Получение списка товаров на странице")
        try:
            items = self.driver.find_elements(*self.INVENTORY_ITEMS)
            logger.info(f"Найдено {len(items)} товаров")
            return items
        except Exception as e:
            logger.error(f"Ошибка при получении товаров: {e}")
            raise

    def go_to_cart(self):
        """Переход в корзину"""
        logger.info("Переход на страницу корзины")
        try:
            self.click(*self.CART_BUTTON)
            logger.info("Успешный переход в корзину")
        except Exception as e:
            logger.error(f"Ошибка при переходе в корзину: {e}")
            raise

    def add_item_to_cart(self, index):
        """Добавляем товар в корзину по индексу"""
        logger.info(f"Добавление товара в корзину с индексом {index}")
        try:
            items = self.get_inventory_items()
            items[index].find_element(*self.ADD_TO_CART_BUTTON).click()
            logger.info(f"Товар с индексом {index} успешно добавлен в корзину")
        except Exception as e:
            logger.error(f"Ошибка при добавлении товара в корзину: {e}")
            raise

    def get_cart_item_count(self):
        """Получаем количество товаров в корзине"""
        logger.info("Получение количества товаров в корзине")
        try:
            count = int(self.get_text(*self.CART_ITEM_COUNT))
            logger.info(f"Количество товаров в корзине: {count}")
            return count
        except ValueError:
            logger.warning("Корзина пуста")
            return 0
        except Exception as e:
            logger.error(f"Ошибка при получении количества товаров в корзине: {e}")
            raise

    def sort_items_by_price(self, option="low-to-high"):
        """Сортировка товаров по цене"""
        logger.info(f"Сортировка товаров по цене: {option}")
        try:
            self.click(*self.SORT_DROPDOWN)
            self.click(By.XPATH, f"//*[text()='{option.capitalize()}']")
            logger.info("Сортировка успешно применена")
        except Exception as e:
            logger.error(f"Ошибка при сортировке товаров: {e}")
            raise
