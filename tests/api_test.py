import allure
import requests

BASE_URL = "https://reqres.in/api"


# Тестирование получения списка пользователей
@allure.feature("API: Пользователи")
@allure.story("Получение списка пользователей (страница 1)")
def test_get_users_page_1():
    response = requests.get(f"{BASE_URL}/users?page=1")
    assert response.status_code == 200
    assert response.json()["page"] == 1

@allure.feature("API: Пользователи")
@allure.story("Получение списка пользователей (страница 2)")
def test_get_users_page_2():
    response = requests.get(f"{BASE_URL}/users?page=2")
    assert response.status_code == 200
    assert response.json()["page"] == 2

@allure.feature("API: Пользователи")
@allure.story("Получение списка пользователей с параметром per_page=5")
def test_get_users_per_page():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=5")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5

# Тестирование получения одного пользователя
@allure.feature("API: Пользователи")
@allure.story("Получение одного пользователя с ID = 2")
def test_get_user_by_id():
    response = requests.get(f"{BASE_URL}/users/2")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2

# Тестирование создания пользователя
@allure.feature("API: Пользователи")
@allure.story("Создание нового пользователя")
def test_create_user():
    payload = {"name": "John", "job": "leader"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "John"
    assert response.json()["job"] == "leader"

# Тестирование обновления пользователя
@allure.feature("API: Пользователи")
@allure.story("Обновление пользователя с ID = 2")
def test_update_user():
    payload = {"name": "John", "job": "developer"}
    response = requests.put(f"{BASE_URL}/users/2", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    assert response.json()["job"] == "developer"

# Тестирование частичного обновления пользователя
@allure.feature("API: Пользователи")
@allure.story("Частичное обновление пользователя с ID = 2")
def test_patch_user():
    payload = {"job": "senior developer"}
    response = requests.patch(f"{BASE_URL}/users/2", json=payload)
    assert response.status_code == 200
    assert response.json()["job"] == "senior developer"

# Тестирование удаления пользователя
@allure.feature("API: Пользователи")
@allure.story("Удаление пользователя с ID = 2")
def test_delete_user():
    response = requests.delete(f"{BASE_URL}/users/2")
    assert response.status_code == 204

# Тестирование получения списка пользователей на пустой странице
@allure.feature("API: Пользователи")
@allure.story("Получение списка пользователей на пустой странице")
def test_get_users_empty_page():
    response = requests.get(f"{BASE_URL}/users?page=999")
    assert response.status_code == 200
    assert response.json()["data"] == []

# Тестирование получения списка пользователей с неверным параметром страницы
@allure.feature("API: Пользователи")
@allure.story("Получение списка пользователей с неверным параметром страницы")
def test_get_users_invalid_page():
    response = requests.get(f"{BASE_URL}/users?page=-1")
    assert response.status_code == 200

# Тестирование получения одного несуществующего пользователя
@allure.feature("API: Пользователи")
@allure.story("Получение одного несуществующего пользователя с ID = 999")
def test_get_non_existent_user():
    response = requests.get(f"{BASE_URL}/users/999")
    assert response.status_code == 404

# Тестирование создания пользователя с недостаточными данными
@allure.feature("API: Пользователи")
@allure.story("Создание пользователя с недостаточными данными")
def test_create_user_invalid_data():
    payload = {"name": "John"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201

# Тестирование обновления пользователя с неверным ID
@allure.feature("API: Пользователи")
@allure.story("Обновление пользователя с неверным ID")
def test_update_user_invalid_id():
    payload = {"name": "John", "job": "developer"}
    response = requests.put(f"{BASE_URL}/users/999", json=payload)
    assert response.status_code == 200

# Тестирование частичного обновления пользователя с неверным ID
@allure.feature("API: Пользователи")
@allure.story("Частичное обновление пользователя с неверным ID")
def test_patch_user_invalid_id():
    payload = {"job": "senior developer"}
    response = requests.patch(f"{BASE_URL}/users/999", json=payload)
    assert response.status_code == 200

# Тестирование удаления несуществующего пользователя
@allure.feature("API: Пользователи")
@allure.story("Удаление несуществующего пользователя с ID = 999")
def test_delete_non_existent_user():
    response = requests.delete(f"{BASE_URL}/users/999")
    assert response.status_code == 204

# Тестирование получения всех пользователей с разными параметрами
@allure.feature("API: Пользователи")
@allure.story("Получение всех пользователей с параметром per_page=10")
def test_get_users_per_page_10():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=10")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 10

# Тестирование получения пользователей с параметром per_page=1
@allure.feature("API: Пользователи")
@allure.story("Получение пользователей с параметром per_page=1")
def test_get_users_per_page_1():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=1")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1

# Тестирование получения страницы 1 с 6 пользователями
@allure.feature("API: Пользователи")
@allure.story("Получение страницы с 6 пользователями")
def test_get_users_per_page_6():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=6")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 6

# Тестирование получения информации о пользователе по ID
@allure.feature("API: Пользователи")
@allure.story("Получение информации о пользователе по ID")
def test_get_user_info_by_id():
    response = requests.get(f"{BASE_URL}/users/3")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 3

# Тестирование того, что создается пользователь с корректными данными
@allure.feature("API: Пользователи")
@allure.story("Создание пользователя с корректными данными")
def test_create_user_with_valid_data():
    payload = {"name": "Alice", "job": "designer"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    assert response.json()["job"] == "designer"

# Тестирование получения списка пользователей с корректной страницей и количеством
@allure.feature("API: Пользователи")
@allure.story("Получение списка пользователей с корректной страницей и количеством")
def test_get_users_correct_page_and_per_page():
    response = requests.get(f"{BASE_URL}/users?page=2&per_page=3")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 3
    assert response.json()["page"] == 2

# Тестирование получения ошибки при неверном параметре page
@allure.feature("API: Пользователи")
@allure.story("Получение ошибки при неверном параметре page")
def test_get_users_invalid_page_param():
    response = requests.get(f"{BASE_URL}/users?page=0")
    assert response.status_code == 200

# Тестирование того, что имя пользователя не может быть пустым
@allure.feature("API: Пользователи")
@allure.story("Создание пользователя с пустым именем")
def test_create_user_empty_name():
    payload = {"name": "", "job": "developer"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201

# Тестирование правильности возврата данных по запросу
@allure.feature("API: Пользователи")
@allure.story("Проверка правильности данных в ответе на запрос пользователя")
def test_check_response_data():
    response = requests.get(f"{BASE_URL}/users/3")
    assert response.status_code == 200
    assert response.json()["data"]["first_name"] == "Emma"
    assert response.json()["data"]["last_name"] == "Wong"
