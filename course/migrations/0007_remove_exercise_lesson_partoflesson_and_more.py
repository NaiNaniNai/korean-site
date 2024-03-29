# Generated by Django 5.0 on 2024-01-22 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0006_alter_answer_options_remove_answer_question_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exercise",
            name="lesson",
        ),
        migrations.CreateModel(
            name="PartOfLesson",
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
                    "title",
                    models.CharField(
                        choices=[
                            ("Словарь", "Словарь"),
                            ("Теоретическая часть", "Теоретическая часть"),
                            ("Практическая часть", "Практическая часть"),
                            ("Домашняя работа", "Домашняя работа"),
                        ],
                        max_length=128,
                        verbose_name="Название",
                    ),
                ),
                ("slug", models.SlugField(max_length=128, verbose_name="Слаг")),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts_of_lesson",
                        to="course.lesson",
                        verbose_name="Урок",
                    ),
                ),
            ],
            options={
                "verbose_name": "Часть урока",
                "verbose_name_plural": "Части урока",
            },
        ),
        migrations.AddField(
            model_name="exercise",
            name="part_of_lesson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercises",
                to="course.partoflesson",
                verbose_name="Части урока",
            ),
        ),
    ]
