from django.contrib import admin
from django.urls import path
from .views import auth_view, register_view

urlpatterns = [
    path("auth/", auth_view, name="auth"),
    path("register/", register_view, name="register"),
]
