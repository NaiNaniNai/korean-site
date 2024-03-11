from django.db.models import QuerySet

from events.models import Events


class EventRepository:
    @staticmethod
    def get_all_events() -> QuerySet[Events]:
        return Events.objects.all()
