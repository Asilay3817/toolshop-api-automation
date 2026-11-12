import allure
from core.base_api import BaseApi

class UsersClient(BaseApi):

    @allure.step("Get all users")
    def get_all(self):
        return self.get("/users")

    @allure.step("User loging")
    def login_user(self, payload: dict):
        return self.post("/users/login", json=payload)