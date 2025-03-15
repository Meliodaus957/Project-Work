import allure
import requests

BASE_URL = "https://reqres.in/api"


# Тестирование получения списка пользователей
@allure.feature("API: Пользователи")
@allure.title("Получение списка пользователей (страница 1)")
@allure.step("Отправка GET-запроса для получения списка пользователей на странице 1")
def test_get_users_page_1():
    response = requests.get(f"{BASE_URL}/users?page=1")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert response.json()["page"] == 1


@allure.feature("API: Пользователи")
@allure.title("Получение списка пользователей (страница 2)")
@allure.step("Отправка GET-запроса для получения списка пользователей на странице 2")
def test_get_users_page_2():
    response = requests.get(f"{BASE_URL}/users?page=2")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert response.json()["page"] == 2


@allure.feature("API: Пользователи")
@allure.title("Получение списка пользователей с параметром per_page=5")
@allure.step("Отправка GET-запроса с параметром per_page=5")
def test_get_users_per_page():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=5")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5


# Тестирование получения одного пользователя
@allure.feature("API: Пользователи")
@allure.title("Получение одного пользователя с ID = 2")
@allure.step("Отправка GET-запроса для получения пользователя с ID = 2")
def test_get_user_by_id():
    response = requests.get(f"{BASE_URL}/users/2")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2


# Тестирование создания пользователя
@allure.feature("API: Пользователи")
@allure.title("Создание нового пользователя")
@allure.step("Отправка POST-запроса для создания нового пользователя")
def test_create_user():
    payload = {"name": "John", "job": "leader"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 201
    assert response.json()["name"] == "John"
    assert response.json()["job"] == "leader"


# Тестирование обновления пользователя
@allure.feature("API: Пользователи")
@allure.title("Обновление пользователя с ID = 2")
@allure.step("Отправка PUT-запроса для обновления пользователя с ID = 2")
def test_update_user():
    payload = {"name": "John", "job": "developer"}
    response = requests.put(f"{BASE_URL}/users/2", json=payload)
    allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    assert response.json()["job"] == "developer"


# Тестирование частичного обновления пользователя
@allure.feature("API: Пользователи")
@allure.title("Частичное обновление пользователя с ID = 2")
@allure.step("Отправка PATCH-запроса для частичного обновления пользователя с ID = 2")
def test_patch_user():
    payload = {"job": "senior developer"}
    response = requests.patch(f"{BASE_URL}/users/2", json=payload)
    allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert response.json()["job"] == "senior developer"


# Тестирование удаления пользователя
@allure.feature("API: Пользователи")
@allure.title("Удаление пользователя с ID = 2")
@allure.step("Отправка DELETE-запроса для удаления пользователя с ID = 2")
def test_delete_user():
    response = requests.delete(f"{BASE_URL}/users/2")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 204


# Тестирование получения списка пользователей на пустой странице
@allure.feature("API: Пользователи")
@allure.title("Получение списка пользователей на пустой странице")
@allure.step("Отправка GET-запроса на пустую страницу пользователей")
def test_get_users_empty_page():
    response = requests.get(f"{BASE_URL}/users?page=999")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert response.json()["data"] == []


# Тестирование получения одного несуществующего пользователя
@allure.feature("API: Пользователи")
@allure.title("Получение одного несуществующего пользователя с ID = 999")
@allure.step("Отправка GET-запроса для получения несуществующего пользователя с ID = 999")
def test_get_non_existent_user():
    response = requests.get(f"{BASE_URL}/users/999")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 404


# Тестирование создания пользователя с недостаточными данными
@allure.feature("API: Пользователи")
@allure.title("Создание пользователя с недостаточными данными")
@allure.step("Отправка POST-запроса с недостаточными данными")
def test_create_user_invalid_data():
    payload = {"name": "John"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 201


# Тестирование обновления пользователя с неверным ID
@allure.feature("API: Пользователи")
@allure.title("Обновление пользователя с неверным ID")
@allure.step("Отправка PUT-запроса для обновления пользователя с неверным ID")
def test_update_user_invalid_id():
    payload = {"name": "John", "job": "developer"}
    response = requests.put(f"{BASE_URL}/users/999", json=payload)
    allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200


# Тестирование частичного обновления пользователя с неверным ID
@allure.feature("API: Пользователи")
@allure.title("Частичное обновление пользователя с неверным ID")
@allure.step("Отправка PATCH-запроса для частичного обновления пользователя с неверным ID")
def test_patch_user_invalid_id():
    payload = {"job": "senior developer"}
    response = requests.patch(f"{BASE_URL}/users/999", json=payload)
    allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200


# Тестирование удаления несуществующего пользователя
@allure.feature("API: Пользователи")
@allure.title("Удаление несуществующего пользователя с ID = 999")
@allure.step("Отправка DELETE-запроса для удаления несуществующего пользователя с ID = 999")
def test_delete_non_existent_user():
    response = requests.delete(f"{BASE_URL}/users/999")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 204


# Тестирование получения всех пользователей с разными параметрами
@allure.feature("API: Пользователи")
@allure.title("Получение всех пользователей с параметром per_page=10")
@allure.step("Отправка GET-запроса с параметром per_page=10")
def test_get_users_per_page_10():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=10")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 10


# Тестирование получения пользователей с параметром per_page=1
@allure.feature("API: Пользователи")
@allure.title("Получение пользователей с параметром per_page=1")
@allure.step("Отправка GET-запроса с параметром per_page=1")
def test_get_users_per_page_1():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=1")
    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


