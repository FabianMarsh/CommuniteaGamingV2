from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from events.models import Event


def serialize_event(event, include_id=False, include_recurrence=False):
    """Return a dictionary representation of an Event instance."""
    data = {
        "title": event.title,
        "start": f"{event.date}T{event.start_time}",
        "end": f"{event.date}T{event.end_time}",
        "description": event.description,
    }
    if include_id:
        data["id"] = event.id
    if include_recurrence:
        data["recurrence"] = event.recurrence
    return data


def get_event_or_404(event_id):
    """Safely fetch an event by ID or return None if not found."""
    try:
        return Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return None


def generate_recurring_dates(base_date, recurrence, count=5):
    """Generate a list of future dates based on recurrence type."""
    dates = []
    for i in range(1, count + 1):
        if recurrence == "daily":
            dates.append(base_date + timedelta(days=i))
        elif recurrence == "weekly":
            dates.append(base_date + timedelta(weeks=i))
        elif recurrence == "monthly":
            try:
                dates.append(base_date + relativedelta(months=i))
            except ValueError:
                # Fallback for invalid dates (e.g., Feb 30)
                dates.append(base_date.replace(day=28) + relativedelta(months=i))
    return dates
