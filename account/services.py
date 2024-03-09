import datetime
import json
import math

from django.utils import timezone

from account.repositories import UserRepository


class ProfileService:
    """Service for view profile detail"""

    def __init__(self, request):
        self.request = request

    def get(self, slug):
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

        print(month_days_online)
        return month_days_online

    @staticmethod
    def get_week_days_online(profile, now_date) -> dict:
        start_week = now_date - datetime.timedelta(now_date.weekday())
        end_week = start_week + datetime.timedelta(7)
        week_online = UserRepository.get_online_per_week(profile, start_week, end_week)
        week_days_online = {}

        if week_online:
            for day_online in week_online:
                day = day_online.date.day
                time_online = day_online.time_online
                week_days_online[day] = time_online
        print(week_days_online)
        return week_days_online
