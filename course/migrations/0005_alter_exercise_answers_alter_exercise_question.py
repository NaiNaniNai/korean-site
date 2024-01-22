# Generated by Django 5.0 on 2024-01-19 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0004_alter_course_slug_alter_dictionarycourse_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercise",
            name="answers",
            field=models.ManyToManyField(
                blank=True,
                related_name="exercises",
                to="course.answer",
                verbose_name="Ответ",
            ),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="question",
            field=models.ManyToManyField(
                blank=True,
                related_name="exercises",
                to="course.question",
                verbose_name="Вопрос",
            ),
        ),
    ]