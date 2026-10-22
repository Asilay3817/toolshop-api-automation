import allure
from core.base_api import BaseApi

class BrandsClient(BaseApi):

    @allure.step("Get all brands")
    def get_all(self):
        return self.get("/brands")

    @allure.step("Create new brand")
    def create(self, payload: dict):
        return self.post("/brands", json=payload)

    @allure.step("Get brand by id")
    def get_by_id(self, id):
        return self.get(f"/brands/{id}")