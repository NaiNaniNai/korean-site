# Generated by Django 5.0 on 2024-02-13 11:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0013_alter_followingusers_user_onlineuser"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="onlineuser",
            options={
                "verbose_name": "Онлайн пользователя",
                "verbose_name_plural": "Онлайн пользователей",
            },
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="time_online",
        ),
        migrations.AlterField(
            model_name="onlineuser",
            name="date",
            field=models.DateField(verbose_name="Дата"),
        ),
        migrations.AlterField(
            model_name="onlineuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_online",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
