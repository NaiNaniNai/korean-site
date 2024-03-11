from datetime import date, datetime

from django.contrib.auth.models import User
from django.db.models import QuerySet

from account.models import OnlineUser, Teacher


class BaseRepository:
    """Class for view interacting with models in base app"""

    @staticmethod
    def get_online_user_today(user: User, today: date) -> OnlineUser:
        return OnlineUser.objects.filter(user=user, date__day=today).first()

    @staticmethod
    def update_online_user_today(
        user: User, current_time: datetime, time_online: int
    ) -> None:
        OnlineUser.objects.update_or_create(
            user=user,
            date=current_time,
            defaults={
                "time_online": time_online,
            },
        )

    @staticmethod
    def get_all_teacher() -> QuerySet[Teacher]:
        return Teacher.objects.all()
