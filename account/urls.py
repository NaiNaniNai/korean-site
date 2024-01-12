from django.urls import path

from account import views

urlpatterns = [
    path("", views.TestView.as_view(), name="test"),
    path("singin/", views.SinginView.as_view(), name="singin"),
    path("logout/", views.logout_view, name="logout"),
]
