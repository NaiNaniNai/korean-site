from django.contrib import admin

from account.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Model of Custom User in admins panel"""

    list_display = ("username", "first_name", "last_name", "email")
