from django import forms
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from course.models import (
    Course,
    Module,
    Lesson,
    Exercise,
    Question,
    Answer,
    CourseUser,
    LessonUser,
    ExerciseUser,
    PartOfLesson,
    PartOfLessonUser,
    ModuleUser,
)


class ExerciseAdminForm(forms.ModelForm):
    text = forms.CharField(label="Основной текст", widget=CKEditorUploadingWidget())

    class Meta:
        model = Exercise
        fields = "__all__"


class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Course
        fields = "__all__"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Model Course in admin panel"""

    form = CourseAdminForm


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(PartOfLesson)
class PartOfLessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Model Exercise in admin panel"""

    form = ExerciseAdminForm


@admin.register(CourseUser)
class CourseUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ModuleUser)
class ModuleUserAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonUser)
class LessonUserAdmin(admin.ModelAdmin):
    pass


@admin.register(PartOfLessonUser)
class PartOfLessonUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ExerciseUser)
class ExerciseUserAdmin(admin.ModelAdmin):
    pass
