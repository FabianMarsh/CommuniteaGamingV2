from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

from .models import Event
from .utils import (
    serialize_event,
    get_event_or_404,
    generate_recurring_dates,
)
from core.utils import parse_date_string


def events_view(request):
    """Render the events page or return JSON if requested via AJAX."""
    events = Event.objects.all().order_by("date", "start_time")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        events_list = [
            {
                "title": event.title,
                "start": f"{event.date}T{event.start_time}",
                "end": f"{event.date}T{event.end_time}",
                "description": event.description,
            }
            for event in events
        ]
        return JsonResponse(events_list, safe=False)

    return render(request, "events/events.html", {"events": events})


# READ functionality ------------------------------------------------
# TODO: Add is_admin check for admin-only access

def events_json(request):
    """Return all events as JSON for calendar rendering."""
    events = Event.objects.all().order_by("date", "start_time")
    events_list = [
        serialize_event(event, include_id=True, include_recurrence=True)
        for event in events
    ]
    return JsonResponse(events_list, safe=False)


@csrf_exempt
def edit_event(request, event_id):
    """Update an existing event."""
    if request.method == "POST":
        event = get_event_or_404(event_id)
        if not event:
            return JsonResponse({"error": "Event not found"}, status=404)

        event.title = request.POST["title"]
        event.description = request.POST.get("description", "")
        event.date = request.POST["date"]
        event.start_time = request.POST["start_time"]
        event.end_time = request.POST["end_time"]
        event.recurrence = request.POST["recurrence"]
        event.save()

        return JsonResponse({"message": "Event updated successfully!"})


@csrf_exempt
def add_event(request):
    """Create a new event and any recurring instances."""
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST.get("description", "")
        date = request.POST["date"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        recurrence = request.POST["recurrence"]

        # Create the initial event
        event = Event.objects.create(
            title=title,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            recurrence=recurrence,
        )

        # Create recurring instances
        event_date = parse_date_string(date) if isinstance(date, str) else date
        future_dates = generate_recurring_dates(event_date, recurrence)

        for new_date in future_dates:
            Event.objects.create(
                title=title,
                description=description,
                date=new_date,
                start_time=start_time,
                end_time=end_time,
                recurrence=recurrence,
            )

        return redirect("events")


@csrf_exempt
def delete_event(request, event_id):
    """Delete an event by ID."""
    if request.method == "DELETE":
        event = get_event_or_404(event_id)
        if not event:
            return JsonResponse({"error": "Event not found"}, status=404)

        event.delete()
        return JsonResponse({"message": "Event deleted successfully!"})

    return JsonResponse({"error": "Invalid request method"}, status=400)
