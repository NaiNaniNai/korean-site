from django.contrib import admin

from account.models import CustomUser, FollowingUsers


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Model of Custom User in admins panel"""

    list_display = ("id", "username", "email")
    list_display_links = ("username",)


@admin.register(FollowingUsers)
class FollowingUsersAdmin(admin.ModelAdmin):
    """Model of following user in admins panel"""

    list_display = ("user", "following_users")
