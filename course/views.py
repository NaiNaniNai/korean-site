from django.views.generic import ListView, DetailView

from .models import Course


class CourseListView(ListView):
    """List of courses"""

    model = Course
    queryset = Course.objects.filter(is_draft=False)
    template_name = "course_list.html"


class CourseDetailView(DetailView):
    """Detail of course"""

    model = Course
    slug_field = "slug"
    template_name = "course_detail.html"
