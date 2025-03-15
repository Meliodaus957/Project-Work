from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from logger import logger


class CartPage(BasePage):


    def get_cart_items(self):
        """Получаем все элементы товаров в корзине"""
        logger.info("Получение всех товаров из корзины")
        try:
            items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
            logger.info(f"Найдено {len(items)} товаров в корзине")
            return items
        except Exception as e:
            logger.error(f"Ошибка при получении товаров из корзины: {e}")
            raise


    def get_item_names(self):
        """Получаем названия всех товаров в корзине"""
        logger.info("Получение названий всех товаров в корзине")
        try:
            items = self.get_cart_items()
            item_names = []
            for item in items:
                name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
                item_names.append(name_element.text)
            logger.info(f"Названия товаров в корзине: {item_names}")
            return item_names
        except Exception as e:
            logger.error(f"Ошибка при получении названий товаров из корзины: {e}")
            raise
