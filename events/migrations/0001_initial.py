# Generated by Django 5.0 on 2024-03-07 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Events",
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
                ("title", models.CharField(max_length=128, verbose_name="Название")),
                (
                    "description",
                    models.CharField(max_length=1024, verbose_name="Описание"),
                ),
                ("start_date", models.DateTimeField(verbose_name="Дата начала")),
                (
                    "end_date",
                    models.DateTimeField(blank=True, verbose_name="Дата окончания"),
                ),
                (
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Окончилось ли"),
                ),
            ],
            options={
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
            },
        ),
    ]
