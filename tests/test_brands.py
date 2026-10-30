import allure
import pytest

from core.models.brands_model import BrandsModel
from utils.helper import Assertions
from core.payloads.brands import brand_payload


@allure.epic("Brands system API")
class TestBrands:

    @allure.story("Get all brands")
    def test_get_all_brands(self, brands_client):
        """
        in test we are chek tat response len !=0 and status 200
        """
        response = brands_client.get_all()
        assert response.status_code == 200, response.text

        brands = [BrandsModel(**item) for item in response.json()]
        assert len(brands) > 0

    @allure.story("Create brand")
    @pytest.mark.regress
    def test_create_brand(self, brands_client):
        """
        in test we are chek tat brand is created and answer structure equal model
        """
        payload = brand_payload()
        response = brands_client.create(payload)
        assert response.status_code == 201, response.text
        model = BrandsModel(**response.json())
        Assertions.assert_brands_matches(model, payload)

        brand_id = model.id

        get_by_id_response = brands_client.get_by_id(brand_id)
        assert get_by_id_response.status_code == 200, get_by_id_response.text
        Assertions.assert_brands_matches(model, payload)








