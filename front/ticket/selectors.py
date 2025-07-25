from datetime import datetime
from email import header
from core import settings
import requests


def ticket_list(
    token: str,
    page: int = 1,
    page_size: int = 50,
    **kwargs,
):
    url = "api/v1/tickets/tickets_list"
    headers = {"Authorization": f"Token {token}"}
    params = {
        "page": page,
        "page_size": page_size,
        **kwargs,
    }
    print(params)
    response = requests.get(
        url=settings.INTERNAL_API_URL + url, headers=headers, params=params
    )
    print(response.url)
    print(response)
    tickets = response.json()
    for ticket in tickets.get("results"):
        ticket["created_at"] = datetime.fromisoformat(
            ticket["created_at"].split("+")[0]
        )
    return tickets


def ticket_detailed(ticket_id: int, token: str):
    url = f"api/v1/tickets/{ticket_id}"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(
        url=settings.INTERNAL_API_URL + url,
        headers=headers,
    )
    print(response)
    print(response.json())
    return response.json()


def get_departments_choices(token):
    url = settings.INTERNAL_API_URL + "/api/v1/common/departments_list"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    choices = [(item["id"], item["name"]) for item in data]
    return choices


def get_subdivision_choices(token):
    url = settings.INTERNAL_API_URL + "/api/v1/common/subdivisions_list"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    choices = [(item["id"], item["name"]) for item in data]
    return choices
