from django.utils import timezone
from .models import Event

def next_event(band):
    return (Event.objects
            .filter(band=band, starts_at__gte=timezone.now())
            .order_by("starts_at")
            .first())

def next_event_of_kind(band, kind):
    return (Event.objects
            .filter(band=band, kind=kind, starts_at__gte=timezone.now())
            .order_by("starts_at")
            .first())