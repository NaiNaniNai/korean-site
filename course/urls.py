from django.urls import path

from course import views

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    path("<str:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
]
