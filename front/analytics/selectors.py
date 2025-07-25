import requests

from core import settings


def get_subdivision_list(token: str):
    url = "api/v1/common/subdivisions_list"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url=settings.INTERNAL_API_URL + url, headers=headers)
    print(response.url)
    print(response)
    return response.json()
