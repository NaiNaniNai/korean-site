from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import (
    Course,
    Module,
    CourseUser,
    LessonUser,
    ExerciseUser,
    Lesson,
    PartOfLessonUser,
    PartOfLesson,
    Answer,
    Exercise,
)


class CourseListView(ListView):
    """List of courses"""

    model = Course
    queryset = Course.objects.filter(is_draft=False)
    template_name = "course_list.html"


class CourseDetailView(View):
    """Detail info of course"""

    def get(self, request, course_slug):
        course = Course.objects.prefetch_related("modules__lessons").get(
            slug=course_slug
        )
        modules = course.modules.all()
        lessons = []
        for module in modules:
            lessons += list(module.lessons.all())

        lessons_count = len(lessons)
        context = {
            "course": course,
            "modules": modules,
            "lessons_count": lessons_count,
        }

        return render(request, "course_detail.html", context)


class PassingCourseView(View):
    """Passing the course"""

    def get(self, request, course_slug):
        course = get_object_or_404(
            Course.objects.prefetch_related("modules__lessons"), slug=course_slug
        )
        modules = course.modules.all()
        user = request.user
        is_available = False

        context = {
            "is_avialable": is_available,
        }

        if not user.id:
            return render(request, "passing_course.html", context)

        user_course = CourseUser.objects.filter(course=course, user=user).first()
        if user_course:
            is_available = True

        modules_data = []
        for module in modules:
            completed_lessons = LessonUser.objects.filter(
                user=user, lesson__module=module, is_completed=True
            )
            lessons_data = []
            for lesson in module.lessons.all():
                completed_part = PartOfLessonUser.objects.filter(
                    user=user, part_of_lesson__lesson=lesson, is_completed=True
                )
                lessons_data.append(
                    {"lesson": lesson, "completed_part": completed_part}
                )
            modules_data.append(
                {
                    "module": module,
                    "completed_lessons": completed_lessons,
                    "lessons_data": lessons_data,
                }
            )
        context = {
            "course": course,
            "modules": modules,
            "user_course": user_course,
            "is_available": is_available,
            "modules_data": modules_data,
        }
        return render(request, "passing_course.html", context)


class PassingLessonView(View):
    """Passing the lesson"""

    def get(self, request, course_slug, module_slug, lesson_slug):
        course = Course.objects.prefetch_related("modules__lessons").get(
            slug=course_slug
        )
        module = Module.objects.filter(slug=module_slug).first()
        user = request.user
        user_course = None
        if user.id:
            user_course = CourseUser.objects.filter(course=course, user=user).first()
        is_available = False
        if user_course:
            is_available = user_course.is_available
        lesson = Lesson.objects.filter(
            module__course=course, module__slug=module_slug, slug=lesson_slug
        ).first()
        theory_part = PartOfLesson.objects.filter(lesson=lesson, slug="theory").first()
        theory_completed_exercises = ExerciseUser.objects.filter(
            user=user, exercise__part_of_lesson=theory_part, is_completed=True
        )
        practical_part = PartOfLesson.objects.filter(
            lesson=lesson, slug="practical"
        ).first()
        practical_part_completed_exercises = ExerciseUser.objects.filter(
            user=user, exercise__part_of_lesson=practical_part, is_completed=True
        ).values_list("exercise", flat=True)
        homework_part = PartOfLesson.objects.filter(
            lesson=lesson, slug="homework"
        ).first()
        homework_part_completed_exercises = ExerciseUser.objects.filter(
            user=user, exercise__part_of_lesson=homework_part, is_completed=True
        )

        context = {
            "course": course,
            "module": module,
            "lesson": lesson,
            "is_available": is_available,
            "theory_part": theory_part,
            "practical_part": practical_part,
            "homework_part": homework_part,
            "theory_completed_exercises": theory_completed_exercises,
            "practical_part_completed_exercises": practical_part_completed_exercises,
            "homework_part_completed_exercises": homework_part_completed_exercises,
        }
        return render(request, "passing_lesson.html", context)

    def post(self, request, course_slug, module_slug, lesson_slug):
        user = request.user
        if request.POST.get("answer_id"):
            answer_id = request.POST.get("answer_id", None)

            if not answer_id:
                messages.error(request, "Не дан ответ")
                return redirect(
                    reverse(
                        "passing_lesson",
                        kwargs={
                            "course_slug": course_slug,
                            "module_slug": module_slug,
                            "lesson_slug": lesson_slug,
                        },
                    )
                )

            exercise_id = request.POST.get("exercise_id", None)
            exercise = Exercise.objects.filter(id=exercise_id).first()
            answer = Answer.objects.filter(id=answer_id).first()

            if not answer.is_correct:
                messages.error(request, "Неправильный ответ")
                return redirect(
                    reverse(
                        "passing_lesson",
                        kwargs={
                            "course_slug": course_slug,
                            "module_slug": module_slug,
                            "lesson_slug": lesson_slug,
                        },
                    )
                )

            ExerciseUser.objects.update_or_create(
                user=user,
                exercise=exercise,
                defaults={
                    "is_completed": True,
                },
            )

        return redirect(
            reverse(
                "passing_lesson",
                kwargs={
                    "course_slug": course_slug,
                    "module_slug": module_slug,
                    "lesson_slug": lesson_slug,
                },
            )
        )
