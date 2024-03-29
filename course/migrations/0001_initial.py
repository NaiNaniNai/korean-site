# Generated by Django 5.0 on 2024-01-17 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
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
                ("text", models.CharField(max_length=128, verbose_name="Текст ответа")),
                ("is_correct", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.CreateModel(
            name="Course",
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
                    "level",
                    models.CharField(
                        choices=[
                            ("1 уровень", "1 уровень"),
                            ("2 уровень", "2 уровень"),
                            ("3 уровень", "3 уровень"),
                            ("4 уровень", "4 уровень"),
                            ("5 уровень", "5 уровень"),
                            ("6 уровень", "6 уровень"),
                        ],
                        max_length=128,
                        verbose_name="Уровень",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=4096, verbose_name="Описание"),
                ),
                (
                    "poster",
                    models.ImageField(upload_to="posters/", verbose_name="Постер"),
                ),
                (
                    "poster_for_main_page",
                    models.ImageField(
                        upload_to="main_poster/",
                        verbose_name="Постер на главной странице",
                    ),
                ),
                ("price", models.CharField(max_length=64, verbose_name="Цена")),
                (
                    "is_draft",
                    models.BooleanField(default=False, verbose_name="Черновик"),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                ("number", models.CharField(max_length=64, verbose_name="Номер")),
                (
                    "description",
                    models.CharField(max_length=128, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
        migrations.CreateModel(
            name="Question",
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
                    "text",
                    models.CharField(max_length=512, verbose_name="Текст вопроса"),
                ),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.CreateModel(
            name="Word",
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
                    "russian_meaning",
                    models.CharField(max_length=256, verbose_name="Русское значение"),
                ),
                (
                    "korean_meaning",
                    models.CharField(max_length=256, verbose_name="Корейское значение"),
                ),
                (
                    "transcription",
                    models.CharField(max_length=256, verbose_name="Транскрипция"),
                ),
            ],
            options={
                "verbose_name": "Слово",
                "verbose_name_plural": "Слова",
            },
        ),
        migrations.CreateModel(
            name="CourseUser",
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
                    "is_available",
                    models.BooleanField(default=False, verbose_name="Доступен ли"),
                ),
                ("time_active", models.DateField(verbose_name="Срок действия доступа")),
                (
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Пройден ли"),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses_user",
                        to="course.course",
                        verbose_name="Курс",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс пользователя",
                "verbose_name_plural": "Курсы пользователей",
            },
        ),
        migrations.CreateModel(
            name="Exercise",
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
                ("number", models.CharField(max_length=64, verbose_name="Номер")),
                (
                    "text",
                    models.CharField(max_length=8192, verbose_name="Основной текст"),
                ),
                (
                    "audio",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="audio/",
                        verbose_name="Аудиозапись",
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="video/",
                        verbose_name="Видеозапись",
                    ),
                ),
                (
                    "answers",
                    models.ManyToManyField(
                        related_name="exercises",
                        to="course.answer",
                        verbose_name="Ответ",
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises",
                        to="course.lesson",
                        verbose_name="Урок",
                    ),
                ),
                (
                    "question",
                    models.ManyToManyField(
                        related_name="exercises",
                        to="course.question",
                        verbose_name="Вопрос",
                    ),
                ),
            ],
            options={
                "verbose_name": "Упражнение",
                "verbose_name_plural": "Упражнения",
            },
        ),
        migrations.CreateModel(
            name="ExerciseUser",
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
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Пройден ли"),
                ),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises_user",
                        to="course.exercise",
                        verbose_name="Упражнение",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Упражнение пользователя",
                "verbose_name_plural": "Упраженения пользователей",
            },
        ),
        migrations.CreateModel(
            name="LessonUser",
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
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Пройден ли"),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons_user",
                        to="course.lesson",
                        verbose_name="Урок",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок пользователя",
                "verbose_name_plural": "Уроки пользователей",
            },
        ),
        migrations.CreateModel(
            name="Module",
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
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="modules",
                        to="course.course",
                        verbose_name="Курсы",
                    ),
                ),
            ],
            options={
                "verbose_name": "Модуль",
                "verbose_name_plural": "Модули",
            },
        ),
        migrations.AddField(
            model_name="lesson",
            name="module",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lessons",
                to="course.module",
                verbose_name="Модули",
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ManyToManyField(
                related_name="answers", to="course.question", verbose_name="Вопрос"
            ),
        ),
        migrations.CreateModel(
            name="VocabularyUser",
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
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vocabulary",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
                (
                    "word",
                    models.ManyToManyField(
                        related_name="vocabulary",
                        to="course.word",
                        verbose_name="Слово",
                    ),
                ),
            ],
            options={
                "verbose_name": "Словарь пользователя",
                "verbose_name_plural": "Словари пользователей",
            },
        ),
        migrations.CreateModel(
            name="DictionaryLesson",
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
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dictionary_lesson",
                        to="course.lesson",
                        verbose_name="Урок",
                    ),
                ),
                (
                    "word",
                    models.ManyToManyField(
                        related_name="dictionary_lesson",
                        to="course.word",
                        verbose_name="Слово",
                    ),
                ),
            ],
            options={
                "verbose_name": "Словарь урока",
                "verbose_name_plural": "Словари уроков",
            },
        ),
        migrations.CreateModel(
            name="DictionaryCourse",
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
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dictionary_course",
                        to="course.course",
                        verbose_name="Курс",
                    ),
                ),
                (
                    "word",
                    models.ManyToManyField(
                        related_name="dictionary_course",
                        to="course.word",
                        verbose_name="Слово",
                    ),
                ),
            ],
            options={
                "verbose_name": "Словарь курса",
                "verbose_name_plural": "Словари курсов",
            },
        ),
    ]
