import datetime
import json
import math

from django.contrib import messages
from django.utils import timezone

from account.repositories import UserRepository
from project_root.settings import BASE_DIR


class ProfileService:
    """Service for view profile detail"""

    def __init__(self, request):
        self.request = request

    def get(self, slug) -> dict:
        now_date = timezone.localtime(timezone.now())
        user, profile = self.get_user_and_profile(slug)

        if not user.is_authenticated:
            return {
                "profile": profile,
                "is_authenticated": False,
            }

        available_courses = UserRepository.get_courses(profile)
        follows, is_followed = self.get_follows_info(user, profile)
        top_onlines = self.get_top_online(profile, follows, now_date.month)
        courses_data = self.get_courses_data(available_courses)
        month_days_online = self.get_month_days_online(profile, now_date.month)
        week_days_online = self.get_week_days_online(profile, now_date)

        return {
            "profile": profile,
            "is_authenticated": True,
            "available_courses": available_courses,
            "follows": follows,
            "is_followed": is_followed,
            "top_onlines": top_onlines,
            "courses_data": courses_data,
            "month_days_online": json.dumps(month_days_online),
            "week_days_online": json.dumps(week_days_online),
        }

    def get_user_and_profile(self, slug) -> tuple:
        user = UserRepository.get_from_request(self.request)
        profile = UserRepository.get_by_slug(slug)

        return user, profile

    def get_follows_info(self, user, profile) -> tuple:
        follows = UserRepository.get_follows(user)
        is_followed = UserRepository.check_following(user, profile)

        return follows, is_followed

    def get_top_online(self, profile, follows, month) -> list:
        top_online_raws = UserRepository.get_top_online_raw(profile, month)
        top_onlines = []
        onlines_list = []
        follows_list = list(
            map(int, [item[0] for item in follows.values_list("following_users")])
        )

        for top_online_raw in top_online_raws:
            user_id, time_online = top_online_raw
            onlines_list.append(user_id)
            time_online = math.ceil(time_online / 60)
            online_user = UserRepository.get_by_id(user_id)
            top_onlines.append({"user": online_user, "time_online": time_online})

        for follow_list in follows_list:
            if follow_list not in onlines_list:
                online_user = UserRepository.get_by_id(follow_list)
                top_onlines.append({"user": online_user, "time_online": 0})

        return top_onlines

    def get_courses_data(self, available_courses) -> list:
        courses_data = []
        for available_course in available_courses:
            course = available_course.course
            user = available_course.user
            completed_lessons = UserRepository.get_count_completed_lessons(user, course)
            lessons = UserRepository.get_count_of_lessons(course)
            courses_data.append(
                {
                    "course": course,
                    "completed_lessons": completed_lessons,
                    "lessons": lessons,
                }
            )

        return courses_data

    def get_month_days_online(self, profile, month) -> dict:
        month_online = UserRepository.get_online_per_month(profile, month)
        month_days_online = {}

        if month_online:
            for day_online in month_online:
                day = day_online.date.day
                time_online = day_online.time_online
                month_days_online[day] = time_online

        return month_days_online

    def get_week_days_online(self, profile, now_date) -> dict:
        start_week = now_date - datetime.timedelta(now_date.weekday())
        end_week = start_week + datetime.timedelta(7)
        week_online = UserRepository.get_online_per_week(profile, start_week, end_week)
        week_days_online = {}

        if week_online:
            for day_online in week_online:
                day = day_online.date.day
                time_online = day_online.time_online
                week_days_online[day] = time_online

        return week_days_online


class EditProfileService:
    """Service for view profile edit"""

    def __init__(self, request, form):
        self.request = request
        self.form = form

    def get(self, slug) -> dict:
        profile = UserRepository.get_by_slug(slug)
        form = self.form
        return {"profile": profile, "form": form}

    def post(self, slug) -> None:
        profile = UserRepository.get_by_slug(slug)
        date_of_birth, last_name, first_name, avatar = self.get_info_from_request(
            profile
        )
        self.update_user_info(profile, date_of_birth, last_name, first_name, avatar)

    def handle_uploaded_file(self, file) -> None:
        with open(f"{BASE_DIR}/media/avatars/{file.name}", "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    def get_info_from_request(self, profile) -> tuple:
        date_of_birth = profile.date_of_birth
        last_name = profile.last_name
        first_name = profile.first_name
        avatar = profile.avatar
        if self.request.POST.get("date_of_birth"):
            date_of_birth = self.request.POST.get("date_of_birth")
        if self.request.POST.get("last_name"):
            last_name = self.request.POST.get("last_name")
        if self.request.POST.get("first_name"):
            first_name = self.request.POST.get("first_name")
        if self.request.FILES.get("avatar"):
            self.handle_uploaded_file(self.request.FILES["avatar"])
            avatar = self.request.FILES["avatar"]

        return date_of_birth, last_name, first_name, avatar

    def update_user_info(
        self, profile, date_of_birth, last_name, first_name, avatar
    ) -> None:
        UserRepository.update_user_info(
            profile, date_of_birth, last_name, first_name, avatar
        )


class FolloworUnfollowUserService:
    """Service for view a user's follow or unfollow to another user"""

    def __init__(self, request):
        self.request = request

    def get(self, slug) -> messages:
        user = UserRepository.get_from_request(self.request)
        profile = UserRepository.get_by_slug(slug)
        if profile == user:
            return self.get_context_data("error", profile)

        is_followed = UserRepository.check_following(user, profile)
        if is_followed:
            UserRepository.unfollow_user(user, profile)
            return self.get_context_data("unfollow", profile)

        UserRepository.follow_user(user, profile)
        return self.get_context_data("follow", profile)

    def get_context_data(self, message, profile) -> messages:
        if message == "error":
            return messages.error(
                self.request, "Вы не можете подписаться на самого себя!"
            )
        text_message = f"Вы отписались от пользователя {profile.username}"
        if message == "follow":
            text_message = f"Вы подписались на пользователя {profile.username}"
        return messages.success(self.request, text_message)


class ResetPasswordService:
    """Service for view reset password user"""

    def __init__(self, request, form):
        self.request = request
        self.form = form

    def get(self) -> dict:
        return {
            "form": self.form,
        }

    def post(self):
        (
            username,
            email,
            new_password,
            repeat_new_password,
        ) = self.get_info_from_request()
        user, user_email = self.get_user_email(username)
        is_authenticity = self.check_authenticity(
            email, user_email, new_password, repeat_new_password
        )
        if not is_authenticity:
            return self.get_context_data()
        self.change_password(user, new_password)
        return

    def get_info_from_request(self) -> tuple:
        username = self.request.POST.get("username")
        email = self.request.POST.get("email")
        new_password = self.request.POST.get("password")
        repeat_new_password = self.request.POST.get("repeated_password")
        return username, email, new_password, repeat_new_password

    def get_user_email(self, username) -> tuple:
        user = UserRepository.get_user_for_username(username).first()
        if not user:
            return None, None
        user_email = user.email
        return user, user_email

    def check_email_authentication(self, email, user_email) -> bool:
        if email != user_email:
            return False
        return True

    def check_passwords_match(self, new_password, repeat_new_password) -> bool:
        if new_password != repeat_new_password:
            return False
        return True

    def check_authenticity(
        self, email, user_email, new_password, repeat_new_password
    ) -> bool:
        authenticity_email = self.check_email_authentication(email, user_email)
        authenticity_password = self.check_passwords_match(
            new_password, repeat_new_password
        )
        if authenticity_email and authenticity_password:
            return True
        return False

    def change_password(self, user, new_password):
        UserRepository.change_password(user, new_password)

    def get_context_data(self) -> messages:
        return {"Error": "True"}, messages.error(
            self.request, "Ошибка в имени пользователя, электронной почте или пароле."
        )
