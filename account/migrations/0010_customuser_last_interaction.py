# Generated by Django 5.0 on 2024-02-11 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0009_customuser_last_online"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_interaction",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]