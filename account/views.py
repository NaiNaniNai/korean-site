from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse


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
        else:
            return JsonResponse(
                {
                    "Error": "Ошибка или в имени или в пароле",
                }
            )


def logout_view(request):
    """Logout from site"""

    logout(request)
    return redirect(reverse("test"))
