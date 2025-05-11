from django.shortcuts import render
from .models import Event

def events_view(request):
    events = Event.objects.all().order_by("date", "start_time")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        events_list = [
            {
                "title": event.title,
                "start": event.date.strftime("%Y-%m-%d"),
                "description": event.description,
            }
            for event in events
        ]
        return JsonResponse(events_list, safe=False)

    return render(request, "events/events.html", {"events": events})

