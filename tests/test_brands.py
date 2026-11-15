import allure
import pytest

from core.models.brands_model import BrandsModel
from utils.helper import Assertions
from core.payloads.brands import brand_payload


@allure.epic("Brands system API")
class TestBrands:

    @allure.story("Get all brands")
    @pytest.mark.regress
    def test_get_all_brands(self, brands_client):
        """
        Verify that the brands list endpoint returns 200 OK and a non-empty list
        """
        response = brands_client.get_all()
        with allure.step("Verify that the brands list endpoint returns 200 OK"):
            assert response.status_code == 200, response.text

        brands = BrandsModel.parse_list(response)
        with allure.step("Verify that the brands list is not empty"):
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
        with allure.step("Verify that the create brand endpoint returns 201 OK"):
            assert response.status_code == 201, response.text
        model = BrandsModel(**response.json())
        Assertions.assert_brands_matches(model, payload)

        brand_id = model.id

        get_by_id_response = admin_brands_client.get_by_id(brand_id)
        with allure.step("Verify that the return brand by id endpoint returns 200 OK"):
            assert get_by_id_response.status_code == 200, get_by_id_response.text
        Assertions.assert_brands_matches(model, payload)

        delete_by_id_response = admin_brands_client.delete_by_id(brand_id)
        with allure.step("Verify that the delete brand by id endpoint returns 204 OK"):
            assert delete_by_id_response.status_code == 204, delete_by_id_response.text

        get_by_id_response = admin_brands_client.get_by_id(brand_id)
        with allure.step("Verify that the return brand by id (after delete) endpoint returns 404"):
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
        with allure.step("Verify that the create brand endpoint returns 422 without required item"):
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
        brands_list = BrandsModel.parse_list(get_all_brands_response)

        found_brand = next((b for b in brands_list if b.id == brand_id), None)
        with allure.step(f"Verify that id:{brand_id} is not in the brands list"):
            assert found_brand is None, f"brand with id:{brand_id} was found"


    @allure.story("Update Brand")
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_update_brand(self, brands_client, created_brand):
        """
        Verify that the brand is updated successfully and its data
        matches the update payload when fetched by ID
        """
        brand_id = created_brand["id"]
        payload = brand_payload()
        update_by_id_response = brands_client.update_by_id(brand_id, payload)

        with allure.step("Verify that the update brands by id endpoint returns 200 OK"):
            assert update_by_id_response.status_code == 200, update_by_id_response.text

        get_by_id_response = brands_client.get_by_id(brand_id)
        with allure.step("Verify that the return brand by id endpoint returns 200 OK"):
            assert get_by_id_response.status_code == 200, get_by_id_response.text
        model = BrandsModel(**get_by_id_response.json())
        with allure.step("Verify that the updated brand data matches the payload"):
            Assertions.assert_brands_matches(model, payload)

        get_all_brands_response = brands_client.get_all()
        with allure.step("Verify that the brands list endpoint returns 200 OK"):
            assert get_all_brands_response.status_code == 200, get_all_brands_response.text
        brands_list_model = BrandsModel.parse_list(get_all_brands_response)
        found_brand = next((b for b in brands_list_model if b.id == brand_id), None)

        assert found_brand is not None, f"brand with id:{brand_id} was not found in the list"
        with allure.step("Verify that the updated brand data matches the payload"):
            Assertions.assert_brands_matches(found_brand, payload)


    @allure.story("Update Brand without required item")
    @pytest.mark.regress
    @pytest.mark.smoke
    @pytest.mark.parametrize("field", [
        "name",
        "slug"
    ])
    def test_partial_update_brand(self, brands_client, created_brand, field):
        """
        Verify that the brand can be successfully updated when some optional fields are omitted
        """
        brand_id = created_brand["id"]
        payload = brand_payload()
        del payload[field]
        update_by_id_response = brands_client.update_by_id(brand_id, payload)

        with allure.step(f"Verify that the update brand endpoint returns 200 without '{field}'"):
            assert update_by_id_response.status_code == 200, update_by_id_response.text

        with allure.step(f"Verify the state of the omitted field '{field}' after update"):
            get_response = brands_client.get_by_id(brand_id)
            assert get_response.status_code == 200, get_response.text
            updated_brand = BrandsModel(**get_response.json())

            with allure.step(f"Verify that the provided fields were updated successfully"):
                for key, value in payload.items():
                    assert getattr(updated_brand, key) == value, f"field '{key}' was not updated correctly"

            with allure.step(f"Verify that the omitted field '{field}' remains unchanged"):
                assert getattr(updated_brand, field) == created_brand[field], \
                    f"omitted field '{field}' changed, but it should remain '{created_brand[field]}'"