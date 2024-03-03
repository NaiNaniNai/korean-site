from django.contrib.auth import get_user_model
from django.db import models

from course.choices import LEVEL_CHOICES, PART_OF_LESSON, PART_OF_LESSON_SLUG

User = get_user_model()


class Course(models.Model):
    """Model of courses"""

    title = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    level = models.CharField(
        max_length=128, choices=LEVEL_CHOICES, verbose_name="Уровень"
    )
    description = models.CharField(max_length=4096, verbose_name="Описание")
    poster = models.ImageField(upload_to="posters/", verbose_name="Постер")
    poster_for_main_page = models.ImageField(
        upload_to="main_poster/", verbose_name="Постер на главной странице"
    )
    price = models.CharField(max_length=64, verbose_name="Цена")
    is_draft = models.BooleanField(default=False, verbose_name="Черновик")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.level}-{self.title}"


class Module(models.Model):
    """Model of module"""

    title = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="modules", verbose_name="Курсы"
    )

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return f"{self.course}-{self.title}"


class Lesson(models.Model):
    """Model of lesson"""

    title = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    number = models.CharField(max_length=64, verbose_name="Номер")
    description = models.CharField(max_length=128, verbose_name="Описание")
    module = models.ForeignKey(
        Module, on_delete=models.PROTECT, related_name="lessons", verbose_name="Модули"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.module}-{self.title}"


class PartOfLesson(models.Model):
    """Model of part of lesson"""

    title = models.CharField(
        max_length=128, choices=PART_OF_LESSON, verbose_name="Название"
    )
    slug = models.CharField(
        max_length=128, choices=PART_OF_LESSON_SLUG, verbose_name="Слаг"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="parts_of_lesson",
        verbose_name="Урок",
    )

    class Meta:
        verbose_name = "Часть урока"
        verbose_name_plural = "Части урока"

    def __str__(self):
        return f"{self.lesson}, {self.title}"


class Question(models.Model):
    """Model of question"""

    text = models.CharField(max_length=512, verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Model of answer"""

    text = models.CharField(max_length=128, verbose_name="Текст ответа")
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"{self.question}-{self.text}-{self.is_correct}"


class Exercise(models.Model):
    """Model of exercises"""

    title = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    number = models.CharField(max_length=64, verbose_name="Номер")
    text = models.CharField(max_length=8192, verbose_name="Основной текст")
    audio = models.FileField(
        upload_to="audio/", blank=True, null=True, verbose_name="Аудиозапись"
    )
    video = models.FileField(
        upload_to="video/", blank=True, null=True, verbose_name="Видеозапись"
    )
    part_of_lesson = models.ForeignKey(
        PartOfLesson,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="Части урока",
    )
    question = models.ManyToManyField(
        Question, related_name="exercises", blank=True, verbose_name="Вопрос"
    )
    answers = models.ManyToManyField(
        Answer, related_name="exercises", blank=True, verbose_name="Ответ"
    )

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"

    def __str__(self):
        return f"{self.part_of_lesson}-{self.number}-{self.title}"


class Word(models.Model):
    """Model of word"""

    russian_meaning = models.CharField(max_length=256, verbose_name="Русское значение")
    korean_meaning = models.CharField(max_length=256, verbose_name="Корейское значение")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def __str__(self):
        return f"{self.korean_meaning}-{self.russian_meaning}"


class DictionaryCourse(models.Model):
    """Model of dictionary of course"""

    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="dictionary_course",
        verbose_name="Курс",
    )
    word = models.ManyToManyField(
        Word, related_name="dictionary_course", verbose_name="Слово"
    )

    class Meta:
        verbose_name = "Словарь курса"
        verbose_name_plural = "Словари курсов"

    def __str__(self):
        return f"{self.course}-{self.word}"


class DictionaryLesson(models.Model):
    """Model of dictionary of lesson"""

    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="dictionary_lesson",
        verbose_name="Урок",
    )
    word = models.ManyToManyField(
        Word, related_name="dictionary_lesson", verbose_name="Слово"
    )

    class Meta:
        verbose_name = "Словарь урока"
        verbose_name_plural = "Словари уроков"

    def __str__(self):
        return f"{self.lesson}-{self.word}"


class VocabularyUser(models.Model):
    """Model of Vocabulary of user"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vocabulary",
        verbose_name="Пользователь",
    )
    word = models.ManyToManyField(Word, related_name="vocabulary", verbose_name="Слово")

    class Meta:
        verbose_name = "Словарь пользователя"
        verbose_name_plural = "Словари пользователей"

    def __str__(self):
        return f"{self.user}-{self.word}"


class CourseUser(models.Model):
    """Model of user's course"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_user",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="courses_user",
        verbose_name="Курс",
    )
    is_available = models.BooleanField(default=False, verbose_name="Доступен ли")
    time_active = models.DateField(verbose_name="Срок действия доступа")
    is_completed = models.BooleanField(default=False, verbose_name="Пройден ли")

    class Meta:
        verbose_name = "Курс пользователя"
        verbose_name_plural = "Курсы пользователей"

    def __str__(self):
        return f"{self.user}-{self.course}-{self.is_available}"


class ModuleUser(models.Model):
    """Model of user's moodule"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="modules_user",
        verbose_name="Пользователь",
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="modules_user",
        verbose_name="Модуль",
    )
    is_completed = models.BooleanField(default=False, verbose_name="Пройден ли")

    class Meta:
        verbose_name = "Модуль пользователя"
        verbose_name_plural = "Модули пользователей"

    def __str__(self):
        return f"{self.user} - {self.module} - {self.is_completed}"


class LessonUser(models.Model):
    """Model of user's lesson"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lessons_user",
        verbose_name="Пользователь",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="lessons_user",
        verbose_name="Урок",
    )
    is_completed = models.BooleanField(default=False, verbose_name="Пройден ли")

    class Meta:
        verbose_name = "Урок пользователя"
        verbose_name_plural = "Уроки пользователей"

    def __str__(self):
        return f"{self.user}-{self.lesson}-{self.is_completed}"


class PartOfLessonUser(models.Model):
    """Model of user's part of level"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="parts_of_lesson_user",
        verbose_name="Пользователь",
    )
    part_of_lesson = models.ForeignKey(
        PartOfLesson,
        on_delete=models.CASCADE,
        related_name="parts_of_lesson_user",
        verbose_name="Части урока",
    )
    is_completed = models.BooleanField(default=False, verbose_name="Пройден ли")

    class Meta:
        verbose_name = "Части урока пользователя"
        verbose_name_plural = "Части уроков пользователей"

    def __str__(self):
        return f"{self.user} {self.part_of_lesson} {self.is_completed}"


class ExerciseUser(models.Model):
    """Model of user's lesson"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="exercises_user",
        verbose_name="Пользователь",
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="exercises_user",
        verbose_name="Упражнение",
    )
    is_completed = models.BooleanField(default=False, verbose_name="Пройден ли")

    class Meta:
        verbose_name = "Упражнение пользователя"
        verbose_name_plural = "Упраженения пользователей"

    def __str__(self):
        return f"{self.user}-{self.exercise}-{self.is_completed}"
