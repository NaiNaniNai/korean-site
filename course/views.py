from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .service import (
    CourseListService,
    CourseDetailService,
    PassingCourseService,
    PassingLessonService,
)


class CourseListView(View):
    """List of courses"""

    def get(self, request):
        service = CourseListService(request)
        context = service.get()
        return render(request, "course_list.html", context)


class CourseDetailView(View):
    """Detail info of course"""

    def get(self, request, course_slug):
        service = CourseDetailService(request)
        context = service.get(course_slug)
        return render(request, "course_detail.html", context)


class PassingCourseView(View):
    """Passing the course"""

    def get(self, request, course_slug):
        service = PassingCourseService(request)
        context = service.get(course_slug)
        return render(request, "passing_course.html", context)


class PassingLessonView(View):
    """Passing the lesson"""

    def get(self, request, course_slug, module_slug, lesson_slug):
        service = PassingLessonService(request)
        context = service.get(course_slug, module_slug, lesson_slug)
        return render(request, "passing_lesson.html", context)

    def post(self, request, course_slug, module_slug, lesson_slug):
        service = PassingLessonService(request)
        context = service.post(course_slug, module_slug, lesson_slug)
        return JsonResponse(context)
