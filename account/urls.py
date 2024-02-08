from django.urls import path

from account import views

urlpatterns = [
    path("", views.TestView.as_view(), name="test"),
    path("singin/", views.SinginView.as_view(), name="singin"),
    path("logout/", views.logout_view, name="logout"),
    path("singup/", views.SingupView.as_view(), name="singup"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("<str:profile_slug>/", views.ProfileView.as_view(), name="profile"),
    path(
        "<str:profile_slug>/edit", views.EditProfileView.as_view(), name="edit_profile"
    ),
    path("<slug:profile_slug>/add_following", views.get_following_user, name="follow"),
]
