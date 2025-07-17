import pytest

from pems_web.districts.models import District


@pytest.fixture
def model_District():
    district = District.objects.create(number="1", name="Eureka")

    return district
