from datetime import datetime
import json
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.utils.safestring import mark_safe

from analytics.selectors import get_subdivision_list
from core import settings
from ticket.selectors import ticket_list


def analytics_main_page_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="analytics_main_page.html")


def reports_view(request: HttpRequest):
    token = request.COOKIES.get("auth_token")
    if not token:
        return redirect(to="auth")
    tickets = ticket_list(token=token, **request.GET.dict())
    filters = {}
    for key, values in request.GET.lists():
        if len(values) == 1 and key != "subdivisions":
            filters[key] = values[0]
        else:
            filters[key] = values
    filters_json = mark_safe(json.dumps(filters))
    print(filters_json)
    context = {
        "tickets": tickets,
        "filters": filters_json,
        "subdivision_list": get_subdivision_list(token=token),
        "api_base_url": settings.EXTERNAL_API_URL,
    }

    return render(request=request, template_name="report.html", context=context)


def clastering_view(request: HttpRequest):
    return render(request=request, template_name="clasters_report.html")
