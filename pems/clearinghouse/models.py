from django.db import models


class DataCatalog(models.Model):
    """Defines a data catalog in the Clearinghouse."""

    class Meta:
        verbose_name = "Data Catalog"
        verbose_name_plural = "Data Catalogs"

    id = models.AutoField(primary_key=True)
    name = models.TextField(help_text="The name of this data catalog.")
    slug = models.SlugField(help_text="The unique slug for this data catalog.", unique=True)

    def __str__(self):
        return self.name


class CatalogEntry(models.Model):
    """Defines an entry in a data catalog."""

    class Meta:
        verbose_name = "Catalog Entry"
        verbose_name_plural = "Catalog Entries"

    id = models.AutoField(primary_key=True)
    catalogs = models.ManyToManyField(DataCatalog)
    name = models.TextField(help_text="The name of this catalog entry.")
    slug = models.SlugField(help_text="The unique slug for this catalog entry.", unique=True)

    def __str__(self):
        return self.name
