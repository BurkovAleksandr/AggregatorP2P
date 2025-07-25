from django.forms import ValidationError
import requests
import requests
from django.conf import settings
from core import settings


def auth_user(username: str, password: str):
    url = settings.INTERNAL_API_URL + "api/v1/user/token"
    data = {"username": username, "password": password}
    response = requests.post(url=url, json=data)
    return response


def register_user(
    *args, **kwargs
) -> requests.Response | None:  # Принимаем только один пароль
    """
    Отправляет запрос на внешнее API для регистрации пользователя.
    """
    url = settings.INTERNAL_API_URL + "api/v1/user/register"
    data = kwargs

    try:
        response = requests.post(url=url, json=data, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error calling registration API: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in register_user service: {e}")
        raise
