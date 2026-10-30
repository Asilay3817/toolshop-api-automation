import allure

from allure_commons.types import AttachmentType

class Helper:
    @staticmethod
    def attach_response(response, name: str = ""):
        allure.attach(
            body=response.text,
            name=name,
            attachment_type=AttachmentType.TEXT
        )


class Assertions:
    @staticmethod
    def assert_brands_matches(model, payload: dict):
        assert model.name == payload['name']
        assert model.slug == payload['slug']