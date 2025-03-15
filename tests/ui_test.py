import pytest
from selenium.webdriver.common.by import By

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
import allure


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture()
def inventory_page(driver):
    return InventoryPage(driver)


@pytest.fixture()
def cart_page(driver):
    return CartPage(driver)


@allure.title("Тест отображения страницы товаров после входа")
@allure.step("Проверка загрузки страницы товаров")
def test_inventory_page_after_login(login_page, driver):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_element(*InventoryPage.INVENTORY_ITEMS)

    inventory_items = inventory_page.get_inventory_items()
    assert "Sauce Labs Backpack" in inventory_items[0].text


@allure.title("Тест функциональности выхода")
@allure.step("Выход из приложения")
def test_logout(driver, login_page):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")


    # Используем явное ожидание для кнопки меню
    login_page.click_for_element(By.ID, "react-burger-menu-btn").click()


    login_page.click_for_element(By.ID, 'logout_sidebar_link').click()


    # Убедимся, что на странице логина
    assert "Swag Labs" in driver.title


@allure.title("Тест сортировки товаров по цене")
@allure.step("Сортировка товаров по цене")
def test_sort_by_price(driver, login_page):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)

    # Ждем появления выпадающего списка сортировки
    inventory_page.wait_for_element(*InventoryPage.SORT_DROPDOWN)

    # Кликаем на выпадающий список и выбираем сортировку по цене
    inventory_page.click(*InventoryPage.SORT_DROPDOWN)
    inventory_page.click(By.XPATH, "//*[text()='Price (low to high)']")

    # Подождем, пока список товаров обновится
    inventory_page.wait_for_element(*InventoryPage.INVENTORY_ITEMS)

    inventory_items = inventory_page.get_inventory_items()

    # Проверяем, что первый товар в списке имеет минимальную цену
    first_item_title = inventory_items[0].text
    assert "Sauce Labs Onesie" in first_item_title  # "Sauce Labs Onesie" - это товар с минимальной ценой


@allure.title("Тест входа с валидными учетными данными")
@allure.step("Вход с учетными данными стандартного пользователя")
def test_login_valid(login_page, driver):
    driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_element(*InventoryPage.INVENTORY_ITEMS)

    inventory_items = inventory_page.get_inventory_items()
    # Добавляем список товаров в отчет
    allure.attach(str(inventory_items), name="Список товаров", attachment_type=allure.attachment_type.TEXT)

    assert len(inventory_items) > 0


@allure.title("Тест входа с неверными учетными данными")
@allure.step("Вход с неверными учетными данными")
def test_login_invalid(login_page, driver):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("invalid_user", "wrong_password")

    error_message = login_page.get_error_message()
    # Добавляем сообщение об ошибке в отчет
    allure.attach(error_message, name="Сообщение об ошибке", attachment_type=allure.attachment_type.TEXT)

    assert "Epic sadface" in error_message


@allure.title("Тест перехода в корзину")
@allure.step("Проверка перехода на страницу корзины")
def test_go_to_cart(login_page, driver):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_element(*InventoryPage.CART_BUTTON)
    inventory_page.go_to_cart()

    # Сохраняем содержимое страницы корзины
    allure.attach(driver.page_source, name="Содержимое корзины", attachment_type=allure.attachment_type.HTML)

    assert "Your Cart" in driver.page_source


@allure.title("Тест добавления товара в корзину")
@allure.step("Добавление товара в корзину")
def test_add_item_to_cart(driver, login_page):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)

    cart_item_count = inventory_page.get_cart_item_count()
    # Сохраняем количество товаров в корзине
    allure.attach(str(cart_item_count), name="Количество товаров в корзине", attachment_type=allure.attachment_type.TEXT)

    assert cart_item_count > 0


@allure.title("Тест ошибки при отсутствии учетных данных")
@allure.step("Попытка входа без указания учетных данных")
def test_login_empty(driver, login_page):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("", "")

    error_message = login_page.get_error_message()
    # Сохраняем сообщение об ошибке
    allure.attach(error_message, name="Сообщение об ошибке", attachment_type=allure.attachment_type.TEXT)

    assert "Epic sadface" in error_message


@allure.title("Тест добавления нескольких товаров в корзину")
@allure.step("Добавление нескольких товаров в корзину")
def test_add_multiple_items_to_cart(driver, login_page):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)
    inventory_page.add_item_to_cart(1)

    cart_item_count = inventory_page.get_cart_item_count()
    # Сохраняем количество товаров в корзине
    allure.attach(str(cart_item_count), name="Количество товаров в корзине", attachment_type=allure.attachment_type.TEXT)

    assert cart_item_count == 2
