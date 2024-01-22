from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Course, CourseUser, LessonUser, ExerciseUser


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
        course = Course.objects.prefetch_related("modules__lessons").get(
            slug=course_slug
        )
        modules = course.modules.all()
        user = request.user
        user_course = CourseUser.objects.filter(course=course, user=user).first()
        is_available = False
        if user_course:
            is_available = user_course.is_available
        modules_data = []
        for module in modules:
            completed_lessons = LessonUser.objects.filter(
                user=user, lesson__module=module, is_completed=True
            )
            lessons_data = []
            for lesson in module.lessons.all():
                completed_exercises = ExerciseUser.objects.filter(
                    user=user, exercise__lesson=lesson, is_completed=True
                )
                lessons_data.append(
                    {"lesson": lesson, "completed_exercises": completed_exercises}
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
