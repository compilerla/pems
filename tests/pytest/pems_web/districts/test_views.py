import pytest

from pems_web.districts import views
from pems_web.districts.models import District


class TestIndexView:
    @pytest.fixture
    def view(app_request):
        v = views.IndexView()
        v.setup(app_request)

        return v

    @pytest.mark.django_db
    def test_get_context_data(self, view):

        context = view.get_context_data()

        assert set(context.get("districts").get("all")) == set(District.objects.all())

    def test_template_name(self, view):
        assert view.template_name == "districts/index.html"


class TestDistrictView:

    @pytest.mark.django_db
    def test_get_object(self, app_request, model_District):

        view = views.DistrictView()
        view.setup(app_request, district_number=model_District.number)

        found_object = view.get_object()

        assert found_object == model_District
