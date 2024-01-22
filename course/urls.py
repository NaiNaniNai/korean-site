from django.urls import path

from course import views

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    path("<str:course_slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path(
        "<str:course_slug>/passing",
        views.PassingCourseView.as_view(),
        name="passing_course",
    ),
]
