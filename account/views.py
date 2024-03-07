import json
import math
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from account.forms import SingupForm
from account.models import CustomUser, FollowingUsers, OnlineUser
from course.models import LessonUser, Lesson, CourseUser
from project_root.settings import BASE_DIR


class TestView(View):
    def get(self, request):
        return render(request, "account.html")


class SinginView(View):
    """Login in site"""

    def get(self, request):
        return render(request, "singin.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse("test"))

        messages.error(request, "Ошибка в логине или пароле!")
        return redirect(reverse("singin"))


def logout_view(request):
    """Logout from site"""

    logout(request)
    return redirect(reverse("test"))


class SingupView(FormView):
    """Singup in anime site"""

    form_class = SingupForm
    template_name = "singup.html"
    success_url = reverse_lazy("singin")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ResetPasswordView(View):
    """Reset password"""

    def get(self, request):
        return render(request, "reset_password.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("password1")
        repeat_new_password = request.POST.get("password2")
        user = CustomUser.objects.filter(username=username).first()
        if (
            user
            and user.email == email
            and new_password
            and new_password == repeat_new_password
        ):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Пароль был успешно обновлён.")
            return redirect(reverse("singin"))
        messages.error(
            request, "Ошибка в имени пользователя, электронной почте или пароле."
        )
        return redirect(reverse("reset_password"))


class ProfileView(View):
    """Detail page of profile"""

    def get(self, request, profile_slug):
        user = request.user
        profile = (
            CustomUser.objects.prefetch_related(
                Prefetch(
                    "courses_user",
                    queryset=CourseUser.objects.prefetch_related(
                        "course",
                        "course__modules",
                        "course__modules__lessons",
                    ).filter(is_available=True),
                    to_attr="avaliable_courses",
                ),
                Prefetch("lessons_user", to_attr="completed_lessons"),
            )
            .filter(slug=profile_slug)
            .first()
        )
        is_authenticated = user.is_authenticated

        context = {
            "profile": profile,
            "is_authenticated": is_authenticated,
        }

        if not is_authenticated:
            return render(request, "profile.html", context)

        available_courses = profile.avaliable_courses
        courses_data = []

        month = timezone.now().month
        now_date = datetime.date.today()
        start_week = now_date - datetime.timedelta(now_date.weekday())
        end_week = start_week + datetime.timedelta(7)

        follows = FollowingUsers.objects.filter(user=profile)
        is_followed = FollowingUsers.objects.filter(user=user, following_users=profile)

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

        top_onlines = []
        follows_list = list(
            map(int, [item[0] for item in follows.values_list("following_users")])
        )
        onlines_list = []

        for top_online_raw in top_online_raws:
            user_id, time_online = top_online_raw
            onlines_list.append(user_id)
            time_online = math.ceil(time_online / 60)
            online_user = CustomUser.objects.filter(id=user_id).first()
            top_onlines.append({"user": online_user, "time_online": time_online})

        for follow_list in follows_list:
            if follow_list not in onlines_list:
                online_user = CustomUser.objects.filter(id=follow_list).first()
                top_onlines.append({"user": online_user, "time_online": 0})

        for available_course in available_courses:
            course = available_course.course
            completed_lessons = LessonUser.objects.filter(
                user=user, lesson__module__course=course
            ).count()
            lessons = Lesson.objects.filter(module__course=course).count()
            courses_data.append(
                {
                    "course": course,
                    "completed_lessons": completed_lessons,
                    "lessons": lessons,
                }
            )

        month_online_profile = OnlineUser.objects.filter(
            user=profile, date__month=month
        )
        month_days_online = {}

        if month_online_profile:
            for month_date_online in month_online_profile:
                day_online = month_date_online.date.day
                time_online = month_date_online.time_online
                month_days_online[day_online] = time_online

        week_online_profile = OnlineUser.objects.filter(
            user=profile, date__range=[start_week, end_week]
        )
        week_days_online = {}

        if week_online_profile:
            for week_date_online in week_online_profile:
                day_online = week_date_online.date.day
                time_online = week_date_online.time_online
                week_days_online[day_online] = time_online

        context = {
            "profile": profile,
            "top_onlines": top_onlines,
            "month_days_online": json.dumps(month_days_online),
            "week_days_online": json.dumps(week_days_online),
            "is_authenticated": is_authenticated,
            "is_followed": is_followed,
            "courses_data": courses_data,
            "follows": follows,
        }

        return render(request, "profile.html", context)


def handle_uploaded_file(f):
    with open(f"{BASE_DIR}/media/avatars/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class EditProfileView(View):
    """Edit page of profile"""

    def get(self, request, profile_slug):
        profile = CustomUser.objects.filter(slug=profile_slug).first()
        context = {
            "profile": profile,
        }

        return render(request, "edit_profile.html", context)

    def post(self, request, profile_slug):
        profile = CustomUser.objects.filter(slug=profile_slug).first()
        date_of_birth = profile.date_of_birth
        last_name = profile.last_name
        first_name = profile.first_name
        avatar = profile.avatar
        if request.POST.get("date_of_birth"):
            date_of_birth = request.POST.get("date_of_birth")
        if request.POST.get("last_name"):
            last_name = request.POST.get("last_name")
        if request.POST.get("first_name"):
            first_name = request.POST.get("first_name")
        if request.FILES.get("avatar"):
            handle_uploaded_file(request.FILES["avatar"])
            avatar = request.FILES["avatar"]
        CustomUser.objects.update_or_create(
            username=profile.username,
            defaults={
                "date_of_birth": date_of_birth,
                "last_name": last_name,
                "first_name": first_name,
                "avatar": avatar,
            },
        )
        return redirect(reverse("profile", kwargs={"profile_slug": profile_slug}))


def get_following_user(request, profile_slug):
    """Add following anime on user"""

    if request.method == "GET":
        followed_user = CustomUser.objects.filter(slug=profile_slug).first()
        user = request.user
        if followed_user == user:
            messages.error(request, "Вы не можете подписаться на самого себя!")
            return redirect(reverse("profile", kwargs={"profile_slug": profile_slug}))
        if FollowingUsers.objects.filter(
            user_id=user.id, following_users_id=followed_user.id
        ):
            FollowingUsers.objects.filter(
                user_id=user.id, following_users_id=followed_user.id
            ).delete()
            messages.success(
                request, f"Вы отписались от пользователя {followed_user.username}"
            )
        else:
            FollowingUsers.objects.filter(user=user).create(
                user_id=user.id, following_users_id=followed_user.id
            )
            messages.success(
                request, f"Вы подписались на пользователя {followed_user.username}"
            )
        return redirect(reverse("profile", kwargs={"profile_slug": profile_slug}))
