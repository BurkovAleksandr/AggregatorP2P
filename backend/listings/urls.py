from django.urls import path

from listings import views


urlpatterns = [
    path("listing/", views.ListingsAPI.as_view(), name="listing"),
]
