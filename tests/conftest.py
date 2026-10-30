import pytest
import allure

from pathlib import Path
from core.endpoints.brands import BrandsClient
from allure_commons.types import AttachmentType

@pytest.fixture
def brands_client():
    return BrandsClient()


@pytest.fixture(autouse=True)
def attach_log_to_allure():
    log_file = Path("logs/test.log")
    log_file.write_text("")

    yield

    if log_file.exists():
        log_content = log_file.read_text(encoding="utf-8")
        allure.attach(
            body=log_content,
            name="test.log",
            attachment_type=AttachmentType.TEXT,
        )