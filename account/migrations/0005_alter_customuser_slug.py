# Generated by Django 5.0 on 2024-01-16 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_customuser_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="slug",
            field=models.CharField(
                blank=True, max_length=128, unique=True, verbose_name="Слаг"
            ),
        ),
    ]
