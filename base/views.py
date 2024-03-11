from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from base.service import UpdateLastOnlineService, IndexPageService


def update_last_online(request):
    service = UpdateLastOnlineService(request)
    context = service.get()
    return JsonResponse(context)


class IndexPageView(View):
    """View of index page"""

    def get(self, request):
        service = IndexPageService(request)
        context = service.get()
        return render(request, "index.html", context)
