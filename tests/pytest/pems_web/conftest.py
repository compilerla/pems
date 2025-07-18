import pytest

from pems_web.districts.models import District


@pytest.fixture
def app_request(rf):
    """
    Fixture creates and initializes a new Django request object similar to a real application request.
    """
    # create a request for the path, initialize
    app_request = rf.get("/some/arbitrary/path")

    return app_request


@pytest.fixture
def model_District():
    district = District.objects.create(number="1", name="Eureka")

    return district
