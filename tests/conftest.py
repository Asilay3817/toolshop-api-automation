import pytest

from core.endpoints.brands import BrandsClient

@pytest.fixture
def brands_client():
    return BrandsClient()