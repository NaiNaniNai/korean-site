from django.db.models import QuerySet

from course.models import (
    Course,
    Module,
    Lesson,
    CourseUser,
    LessonUser,
    PartOfLessonUser,
)
from django.contrib.auth.models import User


class CourseRepository:
    """Class for interacting with the course model"""

    @staticmethod
    def get_by_id(id: int) -> Course:
        return Course.objects.filter(id=id)

    @staticmethod
    def get_by_slug(slug: str) -> Course:
        return Course.objects.filter(slug=slug).prefetch_related(
            "modules", "modules__lessons", "modules__lessons__parts_of_lesson"
        )

    @staticmethod
    def get_all_course() -> QuerySet[Course]:
        return Course.objects.filter(is_draft=False)

    @staticmethod
    def get_modules_of_course(course: Course) -> QuerySet[Module]:
        return course.modules.all()

    @staticmethod
    def get_lessons_of_module(module: Module) -> QuerySet[Lesson]:
        return module.lessons.all()

    @staticmethod
    def get_count_lessons_of_module(module: Module) -> int:
        return module.lessons.count()

    @staticmethod
    def check_available_course(user: User, course: Course) -> bool:
        user_course = CourseUser.objects.filter(user=user, course=course)
        if not user_course:
            return False
        return True

    @staticmethod
    def get_user_completed_lessons_of_module(
        user: User, module: Module
    ) -> QuerySet[LessonUser]:
        return LessonUser.objects.filter(
            user=user, lesson__module=module, is_completed=True
        )

    @staticmethod
    def get_user_completed_part_of_lessons(
        user: User, lesson: Lesson
    ) -> QuerySet[PartOfLessonUser]:
        return PartOfLessonUser.objects.filter(user=user, part_of_lesson__lesson=lesson)
