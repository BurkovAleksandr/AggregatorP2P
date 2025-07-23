from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ParserAccount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="parser_accounts"
    )

    parser_type = models.CharField(
        max_length=50, choices=[("paylonium", "Paylonium"), ("p4u", "P2P4U"), ...]
    )
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    extra_data = models.JSONField(default=dict, blank=True)

    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("parser_type", "login")
