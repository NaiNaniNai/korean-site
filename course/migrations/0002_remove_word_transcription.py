# Generated by Django 5.0 on 2024-01-17 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="word",
            name="transcription",
        ),
    ]
