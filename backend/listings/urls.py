from django.urls import path

from listings import views


urlpatterns = [
    path("listings/", views.ListingsAPI.as_view()),
]
