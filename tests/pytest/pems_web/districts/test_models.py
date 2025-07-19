import pytest


@pytest.mark.django_db
def test_District_str(model_District):
    assert str(model_District) == "1 - Eureka"
