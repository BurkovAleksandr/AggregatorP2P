from datetime import datetime
from django import http
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, response, request
from .selectors import get_departments_choices, get_subdivision_choices
from core import settings
import ticket
from .forms import CreateTicketForm
from .selectors import ticket_list, ticket_detailed

# Create your views here.


def ticket_list_view(request: request.HttpRequest) -> response.HttpResponse:
    token = request.COOKIES.get("auth_token")
    if not token:
        # нет токена — пользователь не аутентифицирован
        return redirect(to="auth")
    # Дефолтные значения и валидация
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 50))
    status = "Created"
    if request.GET.get("status", None):
        status = request.GET.get("status", None)
    tickets = ticket_list(token=token, page=page, page_size=page_size, status=status)
    # print(tickets)
    context = {"tickets": tickets, "page_size": page_size, "status": status}
    return render(request=request, template_name="ticket_list.html", context=context)


def ticket_detailed_view(
    request: request.HttpRequest, ticket_id: int
) -> response.HttpResponse:
    token = request.COOKIES.get("auth_token")
    if not token:
        # нет токена — пользователь не аутентифицирован
        return redirect(to="auth")
    ticket = ticket_detailed(ticket_id=ticket_id, token=token)
    ticket["created_at"] = datetime.fromisoformat(ticket["created_at"].split("+")[0])
    context = {
        "ticket": ticket,
        "api_base_url": settings.EXTERNAL_API_URL,
    }
    return render(
        request=request, template_name="ticket_detailed.html", context=context
    )


def analytic_view(request: request.HttpRequest) -> response.HttpResponse:
    token = request.COOKIES.get("auth_token")
    if not token:
        # нет токена — пользователь не аутентифицирован
        return redirect(to="auth")
    # Дефолтные значения и валидация
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 50))
    tickets = ticket_list(token=token, page=page, page_size=page_size)
    # print(tickets)
    context = {"tickets": tickets, "page_size": page_size}
    return render(request=request, template_name="analytics.html", context=context)


def create_ticket_form(request: request.HttpRequest) -> response.HttpResponse:
    token = request.COOKIES.get("auth_token")
    if not token:
        # нет токена — пользователь не аутентифицирован
        return redirect(to="auth")
    department_choices = get_departments_choices(token=token)
    subdivision_choices = get_subdivision_choices(token=token)

    create_ticket_form = CreateTicketForm(
        department_choices=department_choices,
        subdivissions_choises=subdivision_choices,
    )
    context = {
        "create_ticket_form": create_ticket_form,
        "api_base_url": settings.EXTERNAL_API_URL,
    }
    return render(request=request, template_name="create_ticket.html", context=context)


def change_ticket_status(request: HttpRequest):
    return HttpResponse("Penis")


def add_comment_view(request: HttpRequest):
    return HttpResponse("Penis")
