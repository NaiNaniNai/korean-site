from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Model of User"""

    last_name = models.CharField(max_length=128, verbose_name="Фамилия")
    first_name = models.CharField(max_length=128, verbose_name="Имя")
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default_avatar.png",
        blank=True,
        verbose_name="Аватар",
    )
    groups = models.ManyToManyField(
        "auth.Group", related_name="users", blank=True, verbose_name="Группы"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="users", blank=True, verbose_name="Права"
    )

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
