from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "email",
        "name",
        "surname",
        "phone",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "email",
        "name",
        "surname",
        "phone",
    )

    ordering = ("id",)

    readonly_fields = ("date_joined",)

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "email",
                    "password",
                    "name",
                    "surname",
                    "avatar",
                    "phone",
                    "about",
                    "github_url",
                ),
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": (
                    "favorites",
                    "date_joined",
                ),
            },
        ),
    )
