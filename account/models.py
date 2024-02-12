from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    last_online = models.DateTimeField(
        blank=True, null=True, verbose_name="Последне время онлайна"
    )
    last_interaction = models.DateTimeField(
        blank=True, null=True, verbose_name="Последнее время взаимодействия"
    )
    time_online = models.IntegerField(
        default=0, verbose_name="Время онлайна пользователя"
    )

    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
        return False

    def get_online_info(self):
        if self.is_online():
            return _("Онлайн")
        if self.last_online:
            return _("Последнее посещение: {}").format(naturaltime(self.last_online))
        return _("Нет информации")

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
