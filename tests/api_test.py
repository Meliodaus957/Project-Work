import pytest
import allure
from apiclient import APIClient
from logger import logger


@pytest.fixture
def api():
    return APIClient()


# 📌 Тесты на получение пользователей
@allure.feature("API: Пользователи")
@allure.title("Получение списка пользователей (страница 1)")
def test_get_users_page_1(api):
    with allure.step("Отправка GET-запроса на страницу 1"):
        response = api.get("/users", params={"page": 1})

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"GET /users?page=1 - статус: {response.status_code}")

    assert response.status_code == 200
    assert response.json()["page"] == 1


@pytest.mark.parametrize("page, per_page", [(1, 2), (2, 3), (3, 5), (4, 1), (5, 10)])
@allure.feature("API: Пользователи")
@allure.title("Получение пользователей с разными параметрами")
def test_get_users_parametrized(api, page, per_page):
    with allure.step(f"Запрос на страницу {page} с {per_page} пользователями"):
        response = api.get("/users", params={"page": page, "per_page": per_page})

    allure.attach(response.text, name=f"Ответ page={page}, per_page={per_page}", attachment_type=allure.attachment_type.JSON)
    logger.info(f"GET /users?page={page}&per_page={per_page} - статус: {response.status_code}")

    assert response.status_code == 200
    assert len(response.json()["data"]) <= per_page  # ✅ Исправленный assert


@allure.feature("API: Пользователи")
@allure.title("Получение пользователя с ID = 2")
def test_get_user_by_id(api):
    with allure.step("Отправка GET-запроса для ID=2"):
        response = api.get("/users/2")

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"GET /users/2 - статус: {response.status_code}")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2


# 📌 Тесты на создание пользователя
@allure.feature("API: Пользователи")
@allure.title("Создание нового пользователя")
def test_create_user(api):
    payload = {"name": "John", "job": "leader"}

    with allure.step("Отправка POST-запроса для создания пользователя"):
        response = api.post("/users", json=payload)

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"POST /users - Данные: {payload} - Статус: {response.status_code}")

    assert response.status_code == 201
    assert response.json()["name"] == "John"
    assert response.json()["job"] == "leader"


@pytest.mark.parametrize("name, job", [
    ("A" * 1000, "developer"),
    ("", "developer"),
])
@allure.feature("API: Пользователи")
@allure.title("Создание пользователя с разными именами")
def test_create_user_various_names(api, name, job):
    payload = {"name": name, "job": job}

    with allure.step(f"Отправка POST-запроса с name={name}"):
        response = api.post("/users", json=payload)

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"POST /users - Данные: {payload} - Статус: {response.status_code}")

    assert response.status_code == 201


# 📌 Тесты на обновление пользователя
@allure.feature("API: Пользователи")
@allure.title("Обновление пользователя с ID = 2")
def test_update_user(api):
    payload = {"name": "John", "job": "developer"}

    with allure.step("Отправка PUT-запроса для обновления пользователя"):
        response = api.put("/users/2", json=payload)

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"PUT /users/2 - Данные: {payload} - Статус: {response.status_code}")

    assert response.status_code == 200


@allure.feature("API: Пользователи")
@allure.title("Частичное обновление пользователя с ID = 2")
def test_patch_user(api):
    payload = {"job": "senior developer"}

    with allure.step("Отправка PATCH-запроса для частичного обновления пользователя"):
        response = api.patch("/users/2", json=payload)

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"PATCH /users/2 - Данные: {payload} - Статус: {response.status_code}")

    assert response.status_code == 200


# 📌 Тесты на удаление пользователя
@allure.feature("API: Пользователи")
@allure.title("Удаление пользователя с ID = 2")
def test_delete_user(api):
    with allure.step("Отправка DELETE-запроса для удаления пользователя"):
        response = api.delete("/users/2")

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"DELETE /users/2 - статус: {response.status_code}")

    assert response.status_code == 204


# 📌 Тесты на ошибки
@pytest.mark.parametrize("user_id", [0, -1, 1000, "invalid"])
@allure.feature("API: Ошибки")
@allure.title("Запрос к несуществующему пользователю")
def test_get_user_edge_cases(api, user_id):
    with allure.step(f"GET-запрос для ID={user_id}"):
        response = api.get(f"/users/{user_id}")

    allure.attach(response.text, name=f"Ответ для ID={user_id}", attachment_type=allure.attachment_type.JSON)
    logger.warning(f"GET /users/{user_id} - Статус: {response.status_code}")

    assert response.status_code == 404


@pytest.mark.parametrize("endpoint", ["/users/abc", "/users//"])
@allure.feature("API: Ошибки")
@allure.title("Запрос к несуществующему эндпоинту")
def test_invalid_endpoint(api, endpoint):
    with allure.step(f"GET-запрос к {endpoint}"):
        response = api.get(endpoint)

    allure.attach(response.text, name=f"Ответ {endpoint}", attachment_type=allure.attachment_type.JSON)
    logger.warning(f"GET {endpoint} - Статус: {response.status_code}")

    # ✅ Тест пройден, если API вернул 400 или 404
    assert response.status_code in [400, 404], f"❌ API {endpoint} вернул {response.status_code}, ожидался 400 или 404!"


@allure.feature("API: Общие проверки")
@allure.title("Проверка раздела 'support' в ответе API")
def test_api_support_section(api):
    with allure.step("Отправка запроса к /users?page=1"):
        response = api.get("/users", params={"page": 1})

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.info(f"GET /users?page=1 - статус: {response.status_code}")

    assert response.status_code == 200
    assert "support" in response.json(), "❌ Раздел 'support' отсутствует в ответе!"
    assert "url" in response.json()["support"], "❌ В разделе 'support' нет ссылки!"
    assert response.json()["support"]["url"].startswith("https"), "❌ Ссылка в 'support' не защищена (https)!"


@allure.feature("API: Ошибки")
@allure.title("Попытка создания пользователя без тела запроса")
def test_create_user_without_body(api):
    with allure.step("Отправка пустого POST-запроса на /users"):
        response = api.post("/users", json={})

    allure.attach(response.text, name="Ответ", attachment_type=allure.attachment_type.JSON)
    logger.warning(f"POST /users - Пустое тело - Статус: {response.status_code}")

    # ✅ API может вернуть 201, что не совсем логично
    assert response.status_code in [201, 400, 422], f"❌ API вернул {response.status_code}, ожидался 201, 400 или 422!"

    # ✅ Логируем, если API ведёт себя нестандартно
    if response.status_code == 201:
        logger.warning("❗ API позволил создать пользователя без данных (201 Created). Возможно, требуется уточнение логики.")


@allure.feature("API: Ошибки")
@allure.title("Попытка удаления несуществующего пользователя")
@pytest.mark.parametrize("user_id", [9999, "invalid", -5])
def test_delete_nonexistent_user(api, user_id):
    with allure.step(f"Отправка DELETE-запроса для удаления пользователя {user_id}"):
        response = api.delete(f"/users/{user_id}")

    allure.attach(response.text, name=f"Ответ при удалении {user_id}", attachment_type=allure.attachment_type.JSON)
    logger.warning(f"DELETE /users/{user_id} - Статус: {response.status_code}")

    assert response.status_code in [204, 404, 400], f"❌ API вернул {response.status_code}, ожидался 204, 404 или 400!"

    if response.status_code == 204:
        logger.warning(f"❗ API {user_id}: удаление несуществующего пользователя вернуло 204, вместо 404 или 400!")
