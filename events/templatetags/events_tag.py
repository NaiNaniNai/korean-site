from django import template

from events.service import EventsService

register = template.Library()


@register.inclusion_tag("tags/events.html")
def get_events():
    """Output the events"""

    service = EventsService()
    context = service.get_all_events()
    return context
