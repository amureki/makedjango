from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.functions import Collate

from users.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "username")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "username", "is_staff")
    search_fields = ("email_deterministic", "username_deterministic")
    ordering = ("email",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                email_deterministic=Collate("email", collation="und-x-icu"),
                username_deterministic=Collate("username", collation="und-x-icu"),
            )
        )


admin.site.register(User, UserAdmin)
