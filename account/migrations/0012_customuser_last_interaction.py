# Generated by Django 5.0 on 2024-02-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0011_remove_customuser_last_interaction_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_interaction",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Последнее время взаимодействия"
            ),
        ),
    ]
