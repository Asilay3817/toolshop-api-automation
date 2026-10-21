import allure

from core.models.brands_model import BrandsModel
from core.payloads.brands import brand_payload


@allure.epic("Brands system API")
class TestBrands:

    @allure.story("Get all brands")
    def test_get_all_brands(self, brands_client):
        response = brands_client.get_all()
        assert response.status_code == 200

        brands = [BrandsModel(**item) for item in response.json()]
        assert len(brands) > 0

    @allure.story("Create brand")
    def test_create_brand(self, brands_client):
        payload = brand_payload()
        response = brands_client.create(payload)
        assert response.status_code == 201
        model = BrandsModel(**response.json())
        assert model.name == payload['name']
        assert model.slug == payload['slug']

