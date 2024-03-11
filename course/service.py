from account.repository import UserRepository
from course.repository import CourseRepository


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
        course = CourseRepository.get_by_slug(slug).first()
        modules = CourseRepository.get_modules_of_course(course)
        count_of_lessons = self.get_count_of_lessons_in_course(modules)
        return {
            "course": course,
            "modules": modules,
            "count_of_lessons": count_of_lessons,
        }

    def get_count_of_lessons_in_course(self, modules):
        count_of_lessons = 0
        for module in modules:
            count_of_lessons += CourseRepository.get_count_lessons_of_module(module)
        return count_of_lessons


class PassingCourseService:
    """Service for view of user passing course"""

    def __init__(self, request):
        self.request = request

    def get(self, slug) -> dict:
        course = CourseRepository.get_by_slug(slug).first()
        user = UserRepository.get_from_request(self.request)
        is_available = self.check_available_course(user, course)
        if not is_available:
            return {
                "course": course,
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

    def check_available_course(self, user, course) -> bool:
        if not user.id:
            return False
        is_available = CourseRepository.check_available_course(user, course)
        if not is_available:
            return False
        return True

    def get_modules_data(self, user, modules) -> list:
        modules_data = []
        for module in modules:
            completed_lessons = CourseRepository.get_user_completed_lessons_of_module(
                user, module
            )
            lessons = CourseRepository.get_lessons_of_module(module)
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
            completed_part = CourseRepository.get_user_completed_part_of_lessons(
                user, lesson
            )
            lessons_data.append({"lesson": lesson, "completed_part": completed_part})
        return lessons_data
