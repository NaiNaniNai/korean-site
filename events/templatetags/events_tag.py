from django import template


from events.models import Events

register = template.Library()


@register.inclusion_tag("tags/events.html")
def get_events():
    """Output the events"""

    events = Events.objects.all()
    context = {"events": events}
    return context
