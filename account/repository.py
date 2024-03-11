from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import QuerySet

from account.models import FollowingUsers, OnlineUser, CustomUser
from course.models import Course, LessonUser, Lesson


class UserRepository:
    """Class for interacting with the user model"""

    @staticmethod
    def get_by_id(id: int) -> User:
        return get_user_model().objects.get(id=id)

    @staticmethod
    def get_by_slug(slug: str) -> User:
        return get_user_model().objects.get(slug=slug)

    @staticmethod
    def get_from_request(request) -> User:
        return request.user

    @staticmethod
    def get_courses(user: User) -> QuerySet[Course]:
        return (
            user.courses_user.filter(is_available=True)
            .select_related("course")
            .prefetch_related("course__modules", "course__modules__lessons")
            .all()
        )

    @staticmethod
    def check_following(user: User, profile: User) -> QuerySet[FollowingUsers]:
        return FollowingUsers.objects.filter(user=user, following_users=profile)

    @staticmethod
    def get_follows(user: User) -> QuerySet[FollowingUsers]:
        return FollowingUsers.objects.filter(user=user)

    @staticmethod
    def get_top_online_raw(profile: User, month: date) -> QuerySet[OnlineUser]:
        with connection.cursor() as cursor:
            query = f"""
                select ou.user_id as profile_id, Sum(ou.time_online) as time_online
                from account_followingusers as fu
                join account_onlineuser as ou
                on (ou.user_id = fu.following_users_id and fu.user_id = {profile.id}) or ou.user_id = {profile.id}
                where fu.user_id = {profile.id} and extract (month from ou.date::date) = {month}
                group by ou.user_id
                order by time_online DESC;
            """
            cursor.execute(query)
            top_online_raws = cursor.fetchall()
            return top_online_raws

    @staticmethod
    def get_count_completed_lessons(user: User, course: Course) -> int:
        return LessonUser.objects.filter(
            user=user, lesson__module__course=course
        ).count()

    @staticmethod
    def get_count_of_lessons(course: Course) -> int:
        return Lesson.objects.filter(module__course=course).count()

    @staticmethod
    def get_online_per_month(user: User, month: date) -> QuerySet[OnlineUser]:
        return OnlineUser.objects.filter(user=user, date__month=month)

    @staticmethod
    def get_online_per_week(
        user: User, start_week: date, end_week: date
    ) -> QuerySet[OnlineUser]:
        return OnlineUser.objects.filter(user=user, date__range=[start_week, end_week])

    @staticmethod
    def update_user_info(
        user: User, date_of_birth: date, last_name: str, first_name: str, avatar: str
    ):
        CustomUser.objects.update_or_create(
            username=user.username,
            defaults={
                "date_of_birth": date_of_birth,
                "last_name": last_name,
                "first_name": first_name,
                "avatar": avatar,
            },
        )

    @staticmethod
    def follow_user(user: User, profile: User):
        FollowingUsers.objects.create(user=user, following_users=profile)

    @staticmethod
    def unfollow_user(user: User, profile: User):
        FollowingUsers.objects.filter(user=user, following_users=profile).delete()

    @staticmethod
    def get_user_for_username(username: str) -> User:
        return CustomUser.objects.filter(username=username)

    @staticmethod
    def change_password(user: User, new_password: str):
        user.set_password(new_password)
        user.save()
