from django.contrib import admin
from django.urls import path
from mining.views import (
    RegisterView,
    LoginView,
    DataRetrievalView,
    ad_list,
    home,
    ScrapeDataView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("ads/", ad_list, name="ad_list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("data/", DataRetrievalView.as_view(), name="data"),
    path("scrape/", ScrapeDataView.as_view(), name="scrape_data"),
]
