from django.contrib import messages
from django.shortcuts import redirect, render
from django import http

from user.forms import AuthForm, RegisterForm
from user.services import auth_user, register_user


def register_view(
    request: http.HttpRequest,
) -> http.HttpResponse | http.HttpResponseNotAllowed:
    if request.method == "GET":
        register_form = RegisterForm()
        context = {"register_form": register_form}
        return render(
            request=request, context=context, template_name="register_page.html"
        )

    elif request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            cleaned_data = register_form.cleaned_data
            print(cleaned_data)
            try:
                response = register_user(**cleaned_data)
                if response and response.status_code == 201:
                    messages.success(request, "Registration successful!")
                    return redirect("auth")  # Перенаправить на страницу входа
                else:
                    # Обработать ошибку от внешнего API
                    error_message = (
                        response.json().get("detail", "Registration failed.")
                        if response
                        else "Registration failed."
                    )
                    messages.error(request, f"API Error: {error_message}")
                    # Остаемся на странице регистрации с сообщением об ошибке API
                    context = {"register_form": register_form}
                    return render(
                        request=request,
                        context=context,
                        template_name="register_page.html",
                    )

            except Exception as e:  # Ловим другие возможные ошибки сервиса
                messages.error(request, f"An unexpected error occurred: {e}")
                context = {"register_form": register_form}
                return render(
                    request=request, context=context, template_name="register_page.html"
                )

        else:
            context = {"register_form": register_form}
            messages.error(request, "Please correct the errors below.")
            return render(
                request=request, context=context, template_name="register_page.html"
            )
    else:
        return http.HttpResponse("Idi nahui")


def auth_view(
    request: http.HttpRequest,
) -> http.HttpResponse | http.HttpResponseNotAllowed:
    print(request.method)
    if request.method == "GET":
        auth_form = AuthForm()
        context = {"auth_form": auth_form}
        return render(request=request, context=context, template_name="auth_page.html")
    elif request.method == "POST":
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            cleaned_data = auth_form.cleaned_data
            response = auth_user(**cleaned_data)
            if response and response.status_code == 200:
                resp = redirect("tickets-list")
                token = response.json().get("token")
                resp.set_cookie(
                    "auth_token",
                    token,
                    httponly=False,
                    samesite="Lax",
                    secure=False,
                )

                return resp
            else:
                auth_form.add_error(None, "Неверные логин или пароль")

        return render(request, "auth_page.html", {"auth_form": auth_form})
    else:
        return http.HttpResponseNotAllowed(("PATCH", "PUT", "DELETE"))
