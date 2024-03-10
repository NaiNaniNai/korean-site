from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from account.forms import SingupForm, EditProfileForm, ResetPasswordForm
from account.services import (
    ProfileService,
    EditProfileService,
    FolloworUnfollowUserService,
    ResetPasswordService,
)


class SinginView(FormView):
    """View of login in site"""

    form_class = AuthenticationForm
    template_name = "singin.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())


def logout_view(request):
    """Logout from site"""

    logout(request)
    return redirect(reverse("index"))


class SingupView(FormView):
    """View of registration in site"""

    form_class = SingupForm
    template_name = "singup.html"
    success_url = reverse_lazy("singin")

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class ResetPasswordView(View):
    """View of reset password account"""

    def get(self, request):
        form = ResetPasswordForm
        service = ResetPasswordService(request, form)
        context = service.get()

        return render(request, "reset_password.html", context)

    def post(self, request):
        form = ResetPasswordForm
        service = ResetPasswordService(request, form)
        context = service.post()
        if context:
            return redirect(reverse("reset_password"))
        return redirect(reverse("singin"))


class ProfileView(View):
    """Detail page of profile"""

    def get(self, request, profile_slug):
        service = ProfileService(request)
        context = service.get(profile_slug)
        return render(request, "profile.html", context)


class EditProfileView(View):
    """Edit page of profile"""

    def get(self, request, profile_slug):
        form = EditProfileForm
        service = EditProfileService(request, form)
        context = service.get(profile_slug)

        return render(request, "edit_profile.html", context)

    def post(self, request, profile_slug):
        form = EditProfileForm
        service = EditProfileService(request, form)
        service.post(profile_slug)

        return redirect(reverse("profile", kwargs={"profile_slug": profile_slug}))


def follow_or_unfollow_user(request, profile_slug):
    """Following or unfollowing a user from another user"""

    if request.method == "GET":
        service = FolloworUnfollowUserService(request)
        service.get(profile_slug)
        return redirect(reverse("profile", kwargs={"profile_slug": profile_slug}))
