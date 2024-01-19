from django.shortcuts import render
from django.views import View

from .models import Exercise


class TestView(View):
    def get(self, request, slug):
        test = Exercise.objects.filter(slug=slug).first()
        context = {
            "test": test,
        }

        return render(request, "test.html", context)
