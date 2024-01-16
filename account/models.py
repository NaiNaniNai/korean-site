from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Model of User"""

    slug = models.CharField(
        max_length=128, verbose_name="Слаг", unique=True, blank=True
    )
    slug = "231312"
    email = models.EmailField(verbose_name="Почта", unique=True)
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
        return f"{self.username})"
