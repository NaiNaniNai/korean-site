from datetime import timedelta, datetime

from django.http import JsonResponse
from django.utils import timezone


def update_last_online(request):
    if request.user.is_authenticated:
        user = request.user
        current_time = timezone.now()
        online_time = int(request.POST.get("online_time"))
        last_interaction = user.last_interaction
        countdown = datetime(current_time.year, current_time.month, 1, 0, 0)

        if not last_interaction:
            user.last_interaction = countdown
            user.save(update_fields=["last_interaction"])

        if current_time - timedelta(seconds=online_time) > last_interaction:
            user.time_online += online_time
            user.last_interaction = current_time
            user.last_online = current_time
            user.save(update_fields=["time_online", "last_interaction", "last_online"])

        return JsonResponse({"message": "Last online updated successfully"})
    else:
        return JsonResponse({"error": "User is not authenticated"}, status=401)
