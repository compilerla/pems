"""
URLConf for the districts app.
"""

from django.urls import path, re_path

from pems_web.districts import views

app_name = "districts"
urlpatterns = [
    # /districts
    path("", views.IndexView.as_view(), name="index"),
    re_path(r"^(?P<district_number>([1-9]|1[0-2]))$", views.DistrictView.as_view(), name="district"),
]
