from django.contrib import admin

from account.models import CustomUser, FollowingUsers, OnlineUser, Teacher


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Model of Custom User in admin panel"""

    list_display = ("id", "username", "email")
    list_display_links = ("username",)


@admin.register(FollowingUsers)
class FollowingUsersAdmin(admin.ModelAdmin):
    """Model of following user in admin panel"""

    list_display = ("user", "following_users")


@admin.register(OnlineUser)
class OnlineUserAdmin(admin.ModelAdmin):
    """Model of online user in admin panel"""

    list_display = ("user", "date", "time_online")
    list_display_links = ("user",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = ("user",)
    list_display_links = ("user",)
