from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("pems_web.core.urls")),
    path("admin/", admin.site.urls),
    path("districts/", include("pems_web.districts.urls")),
]
