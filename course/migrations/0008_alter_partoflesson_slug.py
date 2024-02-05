# Generated by Django 5.0 on 2024-01-22 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0007_remove_exercise_lesson_partoflesson_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partoflesson",
            name="slug",
            field=models.CharField(
                choices=[
                    ("dictionary", "dictionary"),
                    ("theory", "theory"),
                    ("practical", "practical"),
                    ("homework", "homework"),
                ],
                max_length=128,
                verbose_name="Слаг",
            ),
        ),
    ]
