from django.db.models import QuerySet

from course.models import (
    Course,
    Module,
    Lesson,
    CourseUser,
    LessonUser,
    PartOfLessonUser,
    PartOfLesson,
    ExerciseUser,
    Exercise,
    Answer,
    ModuleUser,
)
from django.contrib.auth.models import User


class CourseRepository:
    """Class for interacting with the course model"""

    @staticmethod
    def get_by_slug(slug: str) -> Course:
        return (
            Course.objects.filter(slug=slug)
            .prefetch_related(
                "modules", "modules__lessons", "modules__lessons__parts_of_lesson"
            )
            .first()
        )

    @staticmethod
    def get_all_course() -> QuerySet[Course]:
        return Course.objects.filter(is_draft=False)

    @staticmethod
    def get_modules_of_course(course: Course) -> QuerySet[Module]:
        return course.modules.all()

    @staticmethod
    def check_available_course(user: User, course: Course) -> bool:
        user_course = CourseUser.objects.filter(user=user, course=course)
        if not user_course:
            return False
        return True

    @staticmethod
    def update_user_course(user: User, course: Course) -> None:
        CourseUser.objects.filter(user=user, course=course).update(is_completed=True)


class ModuleRepository:
    """Class for interacting with the module model"""

    @staticmethod
    def get_by_slug(slug: str) -> Module:
        return Module.objects.filter(slug=slug).first()

    @staticmethod
    def get_lessons_of_module(module: Module) -> QuerySet[Lesson]:
        return module.lessons.all()

    @staticmethod
    def get_count_lessons_of_module(module: Module) -> int:
        return module.lessons.count()

    @staticmethod
    def check_user_module(user: User, module: Module) -> bool:
        if not ModuleUser.objects.filter(user=user, module=module):
            return False
        return True

    @staticmethod
    def create_user_module(user: User, module: Module) -> None:
        ModuleUser.objects.create(user=user, module=module)

    @staticmethod
    def update_user_module(user: User, module: Module) -> None:
        ModuleUser.objects.filter(user=user, module=module).update(is_completed=True)

    @staticmethod
    def get_user_completed_module(user: User, course: Course) -> QuerySet[ModuleUser]:
        return ModuleUser.objects.filter(
            user=user, module__course=course, is_completed=True
        )


class LessonRepository:
    """Class for interacting with the lesson model"""

    @staticmethod
    def get_by_slug(slug: str) -> Lesson:
        return Lesson.objects.filter(slug=slug).first()

    @staticmethod
    def get_by_module(module: Module) -> Lesson:
        return Lesson.objects.filter(module=module).first()

    @staticmethod
    def get_user_completed_lessons_of_module(
        user: User, module: Module
    ) -> QuerySet[LessonUser]:
        return LessonUser.objects.filter(
            user=user, lesson__module=module, is_completed=True
        )

    @staticmethod
    def check_user_lesson(user: User, lesson: Lesson) -> bool:
        if not LessonUser.objects.filter(user=user, lesson=lesson):
            return False
        return True

    @staticmethod
    def create_user_lesson(user: User, lesson: Lesson) -> None:
        LessonUser.objects.create(user=user, lesson=lesson)

    @staticmethod
    def update_user_lesson(user: User, lesson: Lesson) -> None:
        LessonUser.objects.filter(user=user, lesson=lesson).update(is_completed=True)

    @staticmethod
    def get_user_completed_lesson(user: User, module: Module) -> QuerySet[LessonUser]:
        return LessonUser.objects.filter(
            user=user, lesson__module=module, is_completed=True
        )


class PartOfLessonRepository:
    """Class for interacting with the part of lesson model"""

    @staticmethod
    def get_part_of_lesson_by_slug(lesson: Lesson, slug: str) -> PartOfLesson:
        return PartOfLesson.objects.filter(lesson=lesson, slug=slug).first()

    @staticmethod
    def get_by_exercise(lesson: Lesson, exercise: Exercise) -> PartOfLesson:
        return PartOfLesson.objects.filter(
            lesson=lesson, slug=exercise.part_of_lesson.slug
        ).first()

    @staticmethod
    def get_user_completed_part_of_lessons(
        user: User, lesson: Lesson
    ) -> QuerySet[PartOfLessonUser]:
        return PartOfLessonUser.objects.filter(user=user, part_of_lesson__lesson=lesson)

    @staticmethod
    def check_user_part_of_lesson(
        user: PartOfLessonUser, part_of_lesson: PartOfLessonUser
    ) -> bool:
        if not PartOfLessonUser.objects.filter(
            user=user, part_of_lesson=part_of_lesson
        ):
            return False
        return True

    @staticmethod
    def create_user_part_of_lesson(user: User, part_of_lesson: PartOfLesson) -> None:
        PartOfLessonUser.objects.create(user=user, part_of_lesson=part_of_lesson)

    @staticmethod
    def update_user_part_of_lesson(user: User, part_of_lesson: PartOfLesson) -> None:
        PartOfLessonUser.objects.filter(
            user=user, part_of_lesson=part_of_lesson
        ).update(is_completed=True)

    @staticmethod
    def get_user_completed_part_of_lesson(
        user: User, lesson: Lesson
    ) -> QuerySet[PartOfLessonUser]:
        return PartOfLessonUser.objects.filter(
            user=user, part_of_lesson__lesson=lesson, is_completed=True
        )


class ExerciseRepository:
    """Class for interacting with the exercise model"""

    @staticmethod
    def get_by_id(id: int) -> Exercise:
        return Exercise.objects.filter(id=id).first()

    @staticmethod
    def get_user_completed_exercises(
        user: User, part_of_lesson: PartOfLessonUser
    ) -> QuerySet[ExerciseUser]:
        return ExerciseUser.objects.filter(
            user=user, exercise__part_of_lesson=part_of_lesson, is_completed=True
        )

    @staticmethod
    def check_completed(user: User, exercise: Exercise) -> bool:
        is_completed = ExerciseUser.objects.filter(
            user=user, exercise=exercise, is_completed=True
        )
        if not is_completed:
            return False
        return True

    @staticmethod
    def update_of_create(user: User, exercise: Exercise) -> None:
        ExerciseUser.objects.update_or_create(
            user=user,
            exercise=exercise,
            defaults={
                "is_completed": True,
            },
        )


class AnswerRepository:
    """Class for intracting with the answer model"""

    @staticmethod
    def get_by_id(id: int) -> Answer:
        return Answer.objects.filter(id=id).first()

    @staticmethod
    def check_correct(answer: Answer) -> bool:
        is_correct = answer.is_correct
        if not is_correct:
            return False
        return True
