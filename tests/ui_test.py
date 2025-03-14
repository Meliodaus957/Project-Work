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

@allure.title("Test login with valid credentials")
@allure.step("Login with standard user credentials")
def test_login_valid(login_page, driver):
    driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_element(*InventoryPage.INVENTORY_ITEMS)

    inventory_items = inventory_page.get_inventory_items()
    assert len(inventory_items) > 0


@allure.title("Test login with invalid credentials")
@allure.step("Login with invalid user credentials")
def test_login_invalid(login_page, driver):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("invalid_user", "wrong_password")

    error_message = login_page.get_error_message()
    assert "Epic sadface" in error_message


@allure.title("Test inventory page is displayed after login")
@allure.step("Check that inventory page is loaded")
def test_inventory_page_after_login(login_page, driver):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_element(*InventoryPage.INVENTORY_ITEMS)

    inventory_items = inventory_page.get_inventory_items()
    assert "Sauce Labs Backpack" in inventory_items[0].text


@allure.title("Test cart navigation")
@allure.step("Check navigation to the cart page")
def test_go_to_cart(login_page, driver):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_element(*InventoryPage.CART_BUTTON)
    inventory_page.go_to_cart()

    # Проверим, что на странице корзины есть элемент с корзиной
    assert "Your Cart" in driver.page_source


@allure.title("Test adding item to the cart")
@allure.step("Add an item to the cart")
def test_add_item_to_cart(driver, login_page):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)

    cart_item_count = inventory_page.get_cart_item_count()
    assert cart_item_count > 0


@allure.title("Test logout functionality")
@allure.step("Logout from the application")
def test_logout(driver, login_page):
    login_page = LoginPage(driver)
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")


    # Используем явное ожидание для кнопки меню
    login_page.click_for_element(By.ID, "react-burger-menu-btn").click()


    login_page.click_for_element(By.ID, 'logout_sidebar_link').click()


    # Убедимся, что на странице логина
    assert "Swag Labs" in driver.title


@allure.title("Test error for missing credentials")
@allure.step("Try login without credentials")
def test_login_empty(driver, login_page):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("", "")

    error_message = login_page.get_error_message()
    assert "Epic sadface" in error_message


@allure.title("Test adding multiple items to the cart")
@allure.step("Add multiple items to the cart")
def test_add_multiple_items_to_cart(driver, login_page):
    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)
    inventory_page.add_item_to_cart(1)

    cart_item_count = inventory_page.get_cart_item_count()
    assert cart_item_count == 2


@allure.title("Test sorting items by price")
@allure.step("Sort inventory items by price")
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


@allure.title("Test add item to cart and check cart")
@allure.step("Add item to the cart and verify it's in the cart")
def test_add_item_to_cart(driver, cart_page, login_page, inventory_page):

    login_page.driver.get("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")


    # Ждем появления кнопки для добавления товара в корзину
    inventory_page.wait_for_element(By.XPATH, "//button[text()='Add to cart']")

    # Добавляем первый товар в корзину
    add_to_cart_button = driver.find_element(By.XPATH, "//button[text()='Add to cart']")
    add_to_cart_button.click()

    # Проверяем, что иконка корзины отображает количество товаров
    inventory_page.wait_for_element(By.CLASS_NAME, "shopping_cart_badge")
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")

    # Убедимся, что корзина содержит 1 товар
    assert cart_badge.text == "1"

    # Переходим в корзину
    inventory_page.click(By.CLASS_NAME, "shopping_cart_link")


    # Убедимся, что на странице корзины есть хотя бы один товар
    cart_page.wait_for_element(By.CLASS_NAME, "cart_item")

    # Получаем список всех товаров в корзине
    cart_item_names = cart_page.get_item_names()

    # Проверим, что добавленный товар есть в корзине
    assert "Sauce Labs Backpack" in cart_item_names
