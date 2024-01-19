from django.urls import path

from course import views

urlpatterns = [
    path("<str:slug>/", views.TestView.as_view(), name="test"),
]
