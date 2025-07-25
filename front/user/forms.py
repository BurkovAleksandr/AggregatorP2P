from typing import Any
from django import forms
import requests

from core import settings


class AuthForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)


def get_roles():
    url = settings.INTERNAL_API_URL + "api/v1/common/groups_list"
    response = requests.get(url)
    return [(group.get("id"), group.get("name")) for group in response.json()]


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    telegram_id = forms.IntegerField()
    group = forms.ChoiceField(choices=get_roles)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Password"
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Confirm Password"
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation:
            if password != password_confirmation:

                self.add_error(
                    "password_confirmation", "Passwords do not match."
                )  # Ошибка для поля подтверждения

        return cleaned_data
