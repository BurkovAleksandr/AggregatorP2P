from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class PlatformAccount(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    platform = models.ForeignKey(
        "listings.Platform", verbose_name="Платформа", on_delete=models.CASCADE
    )
    login = models.CharField("Логин", max_length=50)
    password = models.CharField("Пароль", max_length=50)
    is_active = models.BooleanField()

    def __repr__(self):
        return f"Аккаунт: {self.user.username}, Платформа: {self.platform.name}"
