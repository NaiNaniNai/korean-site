from events.repository import EventRepository


class EventsService:
    """Service for display events"""

    def get_all_events(self) -> dict:
        events = EventRepository.get_all_events()
        return {"events": events}
