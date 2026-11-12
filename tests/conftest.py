import pytest
import allure

from pathlib import Path
from core.endpoints.brands import BrandsClient
from core.endpoints.users import UsersClient
from allure_commons.types import AttachmentType

from config import setup_logging, LOG_FILE, ADMIN_EMAIL, ADMIN_PASSWORD

setup_logging()

@pytest.fixture
def brands_client():
    return BrandsClient()


@pytest.fixture(autouse=True)
def attach_log_to_allure():
    log_file = Path(LOG_FILE)
    log_file.write_text("")

    yield

    if log_file.exists():
        log_content = log_file.read_text(encoding="utf-8")
        allure.attach(
            body=log_content,
            name="test.log",
            attachment_type=AttachmentType.TEXT,
        )


@pytest.fixture(scope="session")
def auth_client():
    return UsersClient()


@pytest.fixture(scope="function")
def admin_token(auth_client):
    admin_payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }

    response = auth_client.login_user(admin_payload)

    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture
def admin_brands_client(admin_token):
    """
    Return brands_client with admin root
    """
    client = BrandsClient()
    client.session.headers.update({"Authorization": f"Bearer {admin_token}"})
    return client