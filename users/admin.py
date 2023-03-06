from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "username")
    readonly_fields = (
        "last_login",
        "date_joined",
        "id",
        "public_key",
        "private_key",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "public_key",
                    "private_key",
                    "id",
                ),
            },
        ),
        (
            "Permissions",
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
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
