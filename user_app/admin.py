from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_app.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            None,
            {
                'fields': (
                    'imdb_link',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
