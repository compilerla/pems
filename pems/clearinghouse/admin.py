from django.contrib import admin

from pems.clearinghouse import models


admin.site.register(models.DataCatalog)
admin.site.register(models.CatalogEntry)
