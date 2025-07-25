from django.contrib import admin
from django.urls import path
from .views import (
    add_comment_view,
    ticket_detailed,
    ticket_detailed_view,
    ticket_list_view,
    create_ticket_form,
    change_ticket_status,
)

urlpatterns = [
    path("", ticket_list_view, name="tickets-list"),
    path("<int:ticket_id>/", ticket_detailed_view, name="ticket-detailed"),
    path("create_ticket/", create_ticket_form, name="create-ticket"),
    path("add_comment/", add_comment_view, name="add-comment"),
    path("change_ticket_status", change_ticket_status, name="change-ticket-status"),
]
