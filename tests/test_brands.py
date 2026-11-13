import allure
import pytest

from pydantic import TypeAdapter

from core.models.brands_model import BrandsModel
from utils.helper import Assertions
from core.payloads.brands import brand_payload


@allure.epic("Brands system API")
class TestBrands:

    @allure.story("Get all brands")
    @pytest.mark.regress
    def test_get_all_brands(self, brands_client):
        """
        in test we are chek that response len !=0 and status 200
        """
        response = brands_client.get_all()
        assert response.status_code == 200, response.text

        brands = [BrandsModel(**item) for item in response.json()]
        assert len(brands) > 0

    @allure.story("Create brand")
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_create_brand(self, admin_brands_client):
        """
        in test with admin root we are chek that brand is created and answer structure equal model
        after we delete brand by id and check that brand exactly deleted
        """
        payload = brand_payload()
        response = admin_brands_client.create(payload)
        assert response.status_code == 201, response.text
        model = BrandsModel(**response.json())
        Assertions.assert_brands_matches(model, payload)

        brand_id = model.id

        get_by_id_response = admin_brands_client.get_by_id(brand_id)
        assert get_by_id_response.status_code == 200, get_by_id_response.text
        Assertions.assert_brands_matches(model, payload)

        delete_by_id_response = admin_brands_client.delete_by_id(brand_id)
        assert delete_by_id_response.status_code == 204, delete_by_id_response.text

        get_by_id_response = admin_brands_client.get_by_id(brand_id)
        assert get_by_id_response.status_code == 404, get_by_id_response.text


    @allure.story("Create brand without required item")
    @pytest.mark.regress
    @pytest.mark.parametrize("field", [
        "name",
        "slug"
    ])
    def test_create_brand_without_required_item(self, brands_client, field):
        """
        in test we are chek that brand not created without required item
        """
        payload = brand_payload()
        del payload[field]

        response = brands_client.create(payload)
        assert response.status_code == 422, response.text

    @allure.story("Delete brand")
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_delete_brand(self, admin_brands_client, created_brand):
        """
        in test we are chek that brand can be deleted
        after check that brand exactly deleted
        """
        brand_id = created_brand["id"]
        delete_by_id_response = admin_brands_client.delete_by_id(brand_id)
        with allure.step("Verify that the delete brands by id endpoint returns 204"):
            assert delete_by_id_response.status_code == 204, delete_by_id_response.text

        get_by_id_response = admin_brands_client.get_by_id(brand_id)
        with allure.step("Verify that the brands by id endpoint returns 404 after deleted"):
            assert get_by_id_response.status_code == 404, get_by_id_response.text

        get_all_brands_response = admin_brands_client.get_all()
        with allure.step("Verify that the brands list endpoint returns 200 OK"):
            assert get_all_brands_response.status_code == 200, get_all_brands_response.text
        brands_list = TypeAdapter(list[BrandsModel]).validate_python(get_all_brands_response.json())

        found_brand = next((b for b in brands_list if b.id == brand_id), None)
        with allure.step(f"Verify that id:{brand_id} is not in the brands list"):
            assert found_brand is None, f"brand with id:{brand_id} was found"