import pytest

from pems.clearinghouse import models


@pytest.fixture
def data_catalog():
    return models.DataCatalog.objects.create(name="Data Catalog", slug="data-catalog")


@pytest.fixture
def catalog_entry(data_catalog):
    data_catalog.catalogentry_set.create(name="Catalog Entry", slug="catalog-entry")
    return data_catalog.catalogentry_set.first()


@pytest.mark.django_db
class TestDataCatalog:
    def test_str(self, data_catalog):
        assert str(data_catalog) == "Data Catalog"


@pytest.mark.django_db
class TestCatalogEntry:
    def test_str(self, catalog_entry):
        assert str(catalog_entry) == "Catalog Entry"
