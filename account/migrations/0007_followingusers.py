# Generated by Django 5.0 on 2024-01-17 10:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_alter_customuser_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="FollowingUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "following_users",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followed_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Отслеживаемые пользователи",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка на пользователя",
                "verbose_name_plural": "Подписки на пользователя",
            },
        ),
    ]