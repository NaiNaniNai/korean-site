from django.contrib import messages

from account.repository import UserRepository
from course.repository import (
    CourseRepository,
    ModuleRepository,
    LessonRepository,
    PartOfLessonRepository,
    ExerciseRepository,
    AnswerRepository,
)


class CourseListService:
    """Service for view list of courses"""

    def __init__(self, request):
        self.request = request

    def get(self) -> dict:
        return {"courses": CourseRepository.get_all_course()}


class CourseDetailService:
    """Service for detail view of course"""

    def __init__(self, request):
        self.request = request

    def get(self, slug: str) -> dict:
        course = CourseRepository.get_by_slug(slug)
        modules = CourseRepository.get_modules_of_course(course)
        count_of_lessons = self.get_count_of_lessons_in_course(modules)
        return {
            "course": course,
            "modules": modules,
            "count_of_lessons": count_of_lessons,
        }

    def get_count_of_lessons_in_course(self, modules) -> int:
        count_of_lessons = 0
        for module in modules:
            count_of_lessons += ModuleRepository.get_count_lessons_of_module(module)
        return count_of_lessons


class PassingCourseService:
    """Service for view of user passing course"""

    def __init__(self, request):
        self.request = request

    def get(self, slug) -> dict:
        course = CourseRepository.get_by_slug(slug)
        user = UserRepository.get_from_request(self.request)
        is_available = check_available_course(user, course)
        if not is_available:
            return {
                "is_available": False,
            }

        modules = CourseRepository.get_modules_of_course(course)
        modules_data = self.get_modules_data(user, modules)

        return {
            "course": course,
            "modules": modules,
            "is_available": is_available,
            "modules_data": modules_data,
        }

    def get_modules_data(self, user, modules) -> list:
        modules_data = []
        for module in modules:
            completed_lessons = LessonRepository.get_user_completed_lessons_of_module(
                user, module
            )
            lessons = ModuleRepository.get_lessons_of_module(module)
            lessons_data = self.get_lessons_data(user, lessons)
            modules_data.append(
                {
                    "module": module,
                    "completed_lessons": completed_lessons,
                    "lessons_data": lessons_data,
                }
            )
        return modules_data

    def get_lessons_data(self, user, lessons) -> list:
        lessons_data = []
        for lesson in lessons:
            completed_part = PartOfLessonRepository.get_user_completed_part_of_lessons(
                user, lesson
            )
            lessons_data.append({"lesson": lesson, "completed_part": completed_part})
        return lessons_data


class PassingLessonService:
    """Service for view of user passing lesson"""

    def __init__(self, request):
        self.request = request

    def get(self, course_slug, module_slug, lesson_slug) -> dict:
        course = CourseRepository.get_by_slug(course_slug)
        user = UserRepository.get_from_request(self.request)
        is_available = check_available_course(user, course)
        if not is_available:
            return {
                "is_available": False,
            }

        module = ModuleRepository.get_by_slug(module_slug)
        lesson = LessonRepository.get_by_slug(lesson_slug)
        first_part_of_context = {
            "course": course,
            "is_available": is_available,
            "module": module,
            "lesson": lesson,
        }
        second_part_of_context = self.get_part_of_lesson(user, lesson)
        return self.get_context_data(first_part_of_context, second_part_of_context)

    def get_part_of_lesson(self, user, lesson) -> dict:
        theory_part = PartOfLessonRepository.get_part_of_lesson_by_slug(
            lesson, "theory"
        )
        practical_part = PartOfLessonRepository.get_part_of_lesson_by_slug(
            lesson, "practical"
        )
        homework_part = PartOfLessonRepository.get_part_of_lesson_by_slug(
            lesson, "homework"
        )
        parts = [theory_part, practical_part, homework_part]

        (
            theory_completed_exercises,
            practical_part_completed_exercises,
            homework_part_completed_exercises,
        ) = self.get_user_completed_exercises_in_parts(user, parts)
        return {
            "theory_part": theory_part,
            "practical_part": practical_part,
            "homework_part": homework_part,
            "theory_completed_exercises": theory_completed_exercises,
            "practical_part_completed_exercises": practical_part_completed_exercises,
            "homework_part_completed_exercises": homework_part_completed_exercises,
        }

    def get_user_completed_exercises_in_parts(self, user, parts) -> list:
        completed_exercises = []
        for part in parts:
            completed_exercise = ExerciseRepository.get_user_completed_exercises(
                user, part
            ).values_list("exercise", flat=True)
            completed_exercises.append(completed_exercise)
        return completed_exercises

    def get_context_data(self, first_part_of_context, second_part_of_context) -> dict:
        first_part_of_context.update(second_part_of_context)
        context = first_part_of_context
        return context

    def post(self, course_slug, module_slug) -> dict:
        user = UserRepository.get_from_request(self.request)
        answer_id = self.request.POST.get("answer_id", None)
        exercise_id = self.request.POST.get("exercises_id", None)
        exercise = ExerciseRepository.get_by_id(exercise_id)
        if answer_id:
            is_correct = self.check_correct(answer_id)
            if not is_correct:
                messages.error(self.request, "Неправильный ответ")
                return {"fail": True}

        is_completed = self.check_completed(user, exercise)
        if is_completed:
            return {"success": False}

        ExerciseRepository.update_of_create(user, exercise)
        self.update_passing_course(user, course_slug, module_slug, exercise)
        return {"success": True}

    def check_correct(self, answer_id) -> bool:
        answer = AnswerRepository.get_by_id(answer_id)
        is_correct = AnswerRepository.check_correct(answer)
        if not is_correct:
            return False
        return True

    def check_completed(self, user, exercise) -> bool:
        is_completed = ExerciseRepository.check_completed(user, exercise)
        if not is_completed:
            return False
        return True

    def update_passing_course(self, user, course_slug, module_slug, exercise) -> None:
        course = CourseRepository.get_by_slug(course_slug)
        module = ModuleRepository.get_by_slug(module_slug)
        lesson = LessonRepository.get_by_module(module)
        part_of_lesson = PartOfLessonRepository.get_by_exercise(lesson, exercise)
        module_exist = self.check_user_module(user, module)
        if not module_exist:
            self.create_user_module(user, module)
        lesson_exist = self.check_user_lesson(user, lesson)
        if not lesson_exist:
            self.create_user_lesson(user, lesson)
        part_of_lesson_exist = self.check_user_part_of_lesson(user, part_of_lesson)
        if not part_of_lesson_exist:
            self.create_user_part_of_lesson(user, lesson)
        self.complete_part_of_lesson(user, part_of_lesson)
        self.complete_lesson(user, lesson)
        self.complete_module(user, module)
        self.complete_course(user, course)

    def check_user_module(self, user, module) -> bool:
        is_exist = ModuleRepository.check_user_module(user, module)
        if not is_exist:
            return False
        return True

    def create_user_module(self, user, module) -> None:
        ModuleRepository.create_user_module(user, module)

    def check_user_lesson(self, user, lesson) -> bool:
        is_exist = LessonRepository.check_user_lesson(user, lesson)
        if not is_exist:
            return False
        return True

    def create_user_lesson(self, user, lesson) -> None:
        LessonRepository.create_user_lesson(user, lesson)

    def check_user_part_of_lesson(self, user, part_of_lesson) -> bool:
        is_exist = PartOfLessonRepository.check_user_part_of_lesson(
            user, part_of_lesson
        )
        if not is_exist:
            return False
        return True

    def create_user_part_of_lesson(self, user, part_of_lesson) -> None:
        PartOfLessonRepository.create_user_part_of_lesson(user, part_of_lesson)

    def complete_part_of_lesson(self, user, part_of_lesson) -> None:
        exercises_part_of_lesson = list(part_of_lesson.exercises.values_list("id"))
        exercises_part_of_lesson_user = list(
            ExerciseRepository.get_user_completed_exercises(user, part_of_lesson)
            .order_by("exercise")
            .values_list("exercise")
        )
        if exercises_part_of_lesson == exercises_part_of_lesson_user:
            PartOfLessonRepository.update_user_part_of_lesson(user, part_of_lesson)

    def complete_lesson(self, user, lesson) -> None:
        parts_of_lesson = list(lesson.parts_of_lesson.values_list("id"))
        user_parts_of_lesson = list(
            PartOfLessonRepository.get_user_completed_part_of_lesson(user, lesson)
            .order_by("part_of_lesson")
            .values_list("part_of_lesson")
        )
        if parts_of_lesson == user_parts_of_lesson:
            LessonRepository.update_user_lesson(user, lesson)

    def complete_module(self, user, module) -> None:
        lessons_of_module = list(module.lessons.values_list("id"))
        user_lessons_of_module = list(
            LessonRepository.get_user_completed_lesson(user, module)
            .order_by("lesson")
            .values_list("lesson")
        )
        if lessons_of_module == user_lessons_of_module:
            ModuleRepository.update_user_module(user, module)

    def complete_course(self, user, course) -> None:
        modules_of_course = list(course.modules.values_list("id"))
        user_modules_of_course = list(
            ModuleRepository.get_user_completed_module(user, course)
            .order_by("module")
            .values_list("module")
        )
        if modules_of_course == user_modules_of_course:
            CourseRepository.update_user_course(user, course)


def check_available_course(user, course) -> bool:
    if not user.id:
        return False
    is_available = CourseRepository.check_available_course(user, course)
    if not is_available:
        return False
    return True
