from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from account.forms import SingupForm, EditProfileForm
from account.models import CustomUser
from account.services import (
    ProfileService,
    EditProfileService,
    FolloworUnfollowUserService,
)


class SinginView(View):
    """Login in site"""

    def get(self, request):
        return render(request, "singin.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse("index"))

        messages.error(request, "Ошибка в логине или пароле!")
        return redirect(reverse("singin"))


def logout_view(request):
    """Logout from site"""

    logout(request)
    return redirect(reverse("index"))


class SingupView(FormView):
    """Singup in anime site"""

    form_class = SingupForm
    template_name = "singup.html"
    success_url = reverse_lazy("singin")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ResetPasswordView(View):
    """Reset password"""

    def get(self, request):
        return render(request, "reset_password.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("password1")
        repeat_new_password = request.POST.get("password2")
        user = CustomUser.objects.filter(username=username).first()
        if (
            user
            and user.email == email
            and new_password
            and new_password == repeat_new_password
        ):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Пароль был успешно обновлён.")
            return redirect(reverse("singin"))
        messages.error(
            request, "Ошибка в имени пользователя, электронной почте или пароле."
        )
        return redirect(reverse("reset_password"))


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
