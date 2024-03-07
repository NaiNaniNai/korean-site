from datetime import timedelta, datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from account.models import OnlineUser, Teacher


def update_last_online(request):
    if request.user.is_authenticated:
        user = request.user
        current_time = timezone.now()
        online_time = int(request.POST.get("online_time"))
        last_interaction = user.last_interaction
        countdown = datetime(
            current_time.year, current_time.month, current_time.day, 0, 0
        )
        online_user_today = OnlineUser.objects.filter(
            user=user, date__day=current_time.day
        ).first()
        time_online = 0

        if online_user_today:
            time_online = online_user_today.time_online

        if not last_interaction:
            user.last_interaction = countdown
            user.save(update_fields=["last_interaction"])

        if current_time - timedelta(seconds=online_time) > last_interaction:
            OnlineUser.objects.update_or_create(
                user=user,
                date=current_time,
                defaults={
                    "time_online": time_online + online_time,
                },
            )
            user.last_interaction = current_time
            user.last_online = current_time
            user.save(update_fields=["last_interaction", "last_online"])

        return JsonResponse({"message": "Last online updated successfully"})
    else:
        return JsonResponse({"error": "User is not authenticated"}, status=401)


class IndexView(View):
    """View of index page"""

    def get(self, request):
        teachers = Teacher.objects.all()
        context = {
            "teachers": teachers,
        }
        return render(request, "index.html", context)
