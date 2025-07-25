from django.contrib import admin
from django.urls import path

from .views import analytics_main_page_view, reports_view, clastering_view

app_name = "analytics"
urlpatterns = [
    path("", analytics_main_page_view, name="analytic-main-page"),
    path("reports", reports_view, name="reports"),
    path("clustering", clastering_view, name="clustering"),
]
