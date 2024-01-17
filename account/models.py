from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Model of User"""

    slug = models.CharField(max_length=128, verbose_name="Слаг", unique=True)
    email = models.EmailField(verbose_name="Почта", unique=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default_avatar.png",
        blank=True,
        verbose_name="Аватар",
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Дата рождения"
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.username
        super().save(*args, **kwargs)


class FollowingUsers(models.Model):
    """Model of following users"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="following_user",
    )
    following_users = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Отслеживаемые пользователи",
        related_name="followed_user",
    )

    class Meta:
        verbose_name = "Подписка на пользователя"
        verbose_name_plural = "Подписки на пользователя"

    def __str__(self) -> str:
        return f"{self.user} - {self.following_users}"
