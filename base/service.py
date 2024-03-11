from datetime import datetime, timedelta

from django.utils import timezone

from account.repository import UserRepository
from base.repository import BaseRepository


class UpdateLastOnlineService:
    """Service for view of update last online user"""

    def __init__(self, request):
        self.request = request

    def get(self) -> dict:
        user = UserRepository.get_from_request(self.request)
        if not user.is_authenticated:
            return {"error": "User is not authenticated"}

        current_time = timezone.localtime(timezone.now())
        today = current_time.day
        online_time = int(self.request.POST.get("online_time"))
        last_interaction = user.last_interaction
        countdown = datetime(
            current_time.year, current_time.month, current_time.day, 0, 0
        )
        online_user_today = BaseRepository.get_online_user_today(user, today)

        time_online = 0

        if online_user_today:
            time_online = online_user_today.time_online

        if not last_interaction:
            user.last_interaction = countdown
            user.save(update_fields=["last_interaction"])

        if current_time - timedelta(seconds=online_time) > last_interaction:
            BaseRepository.update_online_user_today(
                user, current_time, time_online + online_time
            )
            user.last_interaction = current_time
            user.last_online = current_time
            user.save(update_fields=["last_interaction", "last_online"])

        return {"message": "Last online updated successfully"}


class IndexPageService:
    """Service for view index page"""

    def __init__(self, request):
        self.request = request

    def get(self) -> dict:
        teachers = BaseRepository.get_all_teacher()
        return {
            "teachers": teachers,
        }
