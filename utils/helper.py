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