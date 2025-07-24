from django.contrib import admin
from .models import Platform
from user.models import PlatformAccount


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")


@admin.register(PlatformAccount)
class PlatformAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "platform", "login", "is_active")
    list_filter = ("platform", "is_active")
    search_fields = ("login", "user__username")
