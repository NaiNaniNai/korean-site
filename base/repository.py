from datetime import date, datetime

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone

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


class OnlineUserRepository:
    """Class for interacting with online user model"""

    @staticmethod
    def delete_online_for_the_last_month() -> QuerySet[OnlineUser]:
        current_month = timezone.localtime(timezone.now()).month
        return OnlineUser.objects.filter(date__month__lt=current_month).delete()
