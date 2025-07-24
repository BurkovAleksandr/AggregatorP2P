from django.urls import path

from . import views


urlpatterns = [
    path("accounts/", views.ParserAccountsAPI.as_view(), name="accounts"),
]
