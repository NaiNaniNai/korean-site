from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from account.forms import SingupForm
from account.models import CustomUser
from project_root.settings import BASE_DIR


class TestView(View):
    def get(self, request):
        return render(request, "account.html")


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
            return redirect(reverse("test"))

        messages.error(request, "Ошибка в логине или пароле!")
        return redirect(reverse("singin"))


def logout_view(request):
    """Logout from site"""

    logout(request)
    return redirect(reverse("test"))


class SingupView(FormView):
    """Singup in anime site"""

    form_class = SingupForm
    template_name = "singup.html"
    success_url = reverse_lazy("singin")

    def form_valid(self, form):
        form.save()
        print(form)
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

    def get(self, request, user_slug):
        profile = CustomUser.objects.filter(slug=user_slug).first()
        follows = profile.following_user.all()
        context = {"profile": profile, "follows": follows}

        return render(request, "profile.html", context)


def handle_uploaded_file(f):

    with open(f"{BASE_DIR}/media/avatars/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class EdirProfileView(View):
    """Edit page of profile"""

    def get(self, request, user_slug):
        profile = CustomUser.objects.filter(slug=user_slug).first()
        context = {
            "profile": profile,
        }

        return render(request, "edit_profile.html", context)

    def post(self, request, user_slug):
        profile = CustomUser.objects.filter(slug=user_slug).first()
        date_of_birth = profile.date_of_birth
        last_name = profile.last_name
        first_name = profile.first_name
        avatar = profile.avatar
        if request.POST.get("date_of_birth"):
            date_of_birth = request.POST.get("date_of_birth")
        if request.POST.get("last_name"):
            last_name = request.POST.get("last_name")
        if request.POST.get("first_name"):
            first_name = request.POST.get("first_name")
        if request.FILES.get("avatar"):
            print("ass")
            handle_uploaded_file(request.FILES["avatar"])
            avatar = request.FILES["avatar"]
        print(
            f"Фамилия:{last_name}, Имя:{first_name}, Датарождения:{date_of_birth}, Аватар:{avatar}"
        )
        CustomUser.objects.update_or_create(
            username=profile.username,
            defaults={
                "date_of_birth": date_of_birth,
                "last_name": last_name,
                "first_name": first_name,
                "avatar": avatar,
            },
        )
        return redirect(reverse("test"))
