import requests
import allure
from logger import logger

BASE_URL = "https://reqres.in/api"


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL

    @allure.step("GET запрос к {endpoint} с параметрами: {params}")
    def get(self, endpoint, params=None):
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            allure.attach(response.text, name="Ответ API", attachment_type=allure.attachment_type.JSON)

            if response.status_code == 404:
                logger.warning(f"GET {endpoint} - 404 Not Found")
            else:
                logger.info(f"GET {endpoint} - Статус: {response.status_code}")

            return response
        except requests.RequestException as e:
            logger.error(f"Ошибка GET {endpoint}: {str(e)}")
            raise

    @allure.step("POST запрос к {endpoint} с данными: {json}")
    def post(self, endpoint, json=None):
        try:
            json_data = json or {}  # 🛠 Защита от None
            response = self.session.post(f"{self.base_url}{endpoint}", json=json_data)
            response.raise_for_status()
            allure.attach(str(json_data), name="Запрос", attachment_type=allure.attachment_type.JSON)
            allure.attach(response.text, name="Ответ API", attachment_type=allure.attachment_type.JSON)
            logger.info(f"POST {endpoint} - Данные: {json_data} - Статус: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Ошибка POST {endpoint}: {str(e)}")
            raise

    @allure.step("PUT запрос к {endpoint} с данными: {json}")
    def put(self, endpoint, json=None):
        try:
            json_data = json or {}
            response = self.session.put(f"{self.base_url}{endpoint}", json=json_data)
            response.raise_for_status()
            allure.attach(str(json_data), name="Запрос", attachment_type=allure.attachment_type.JSON)
            allure.attach(response.text, name="Ответ API", attachment_type=allure.attachment_type.JSON)
            logger.info(f"PUT {endpoint} - Данные: {json_data} - Статус: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Ошибка PUT {endpoint}: {str(e)}")
            raise

    @allure.step("PATCH запрос к {endpoint} с данными: {json}")
    def patch(self, endpoint, json=None):
        try:
            json_data = json or {}
            response = self.session.patch(f"{self.base_url}{endpoint}", json=json_data)
            response.raise_for_status()
            allure.attach(str(json_data), name="Запрос", attachment_type=allure.attachment_type.JSON)
            allure.attach(response.text, name="Ответ API", attachment_type=allure.attachment_type.JSON)
            logger.info(f"PATCH {endpoint} - Данные: {json_data} - Статус: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Ошибка PATCH {endpoint}: {str(e)}")
            raise

    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint):
        try:
            response = self.session.delete(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            allure.attach(response.text, name="Ответ API", attachment_type=allure.attachment_type.JSON)
            logger.info(f"DELETE {endpoint} - Статус: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Ошибка DELETE {endpoint}: {str(e)}")
            raise
