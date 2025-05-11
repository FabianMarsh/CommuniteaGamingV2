from django.shortcuts import render
from .models import Event

def events_view(request):
    events = Event.objects.all().order_by("date", "start_time")
    return render(request, "events/events.html", {"events": events})
