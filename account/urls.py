from django.urls import path

from account import views

urlpatterns = [
    path("", views.TestView.as_view(), name="test"),
    path("singin/", views.SinginView.as_view(), name="singin"),
    path("logout/", views.logout_view, name="logout"),
    path("singup/", views.SingupView.as_view(), name="singup"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("<str:username>/", views.ProfileView.as_view(), name="account_detail"),
]
