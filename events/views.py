from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Event
from django.http import JsonResponse
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

def events_view(request):
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


def is_admin(request):
    return JsonResponse({"is_admin": request.user.is_staff})

# READ functionality ------------------------------------------------

def events_json(request):
    events = Event.objects.all().order_by("date", "start_time")

    events_list = [
        {
            "id": event.id,
            "title": event.title,
            "start": f"{event.date}T{event.start_time}",
            "end": f"{event.date}T{event.end_time}",
            "description": event.description,
            "recurrence": event.recurrence
        }
        for event in events
    ]

    return JsonResponse(events_list, safe=False)

@csrf_exempt
def edit_event(request, event_id):
    if request.method == "POST":
        try:
            event = Event.objects.get(id=event_id)
            event.title = request.POST["title"]
            event.description = request.POST.get("description", "")
            event.date = request.POST["date"]
            event.start_time = request.POST["start_time"]
            event.end_time = request.POST["end_time"]
            event.recurrence = request.POST["recurrence"]

            event.save()

            return JsonResponse({"message": "Event updated successfully!"})
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=404)


@csrf_exempt
def add_event(request):
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
            date=date,  # this might be a string initially
            start_time=start_time,
            end_time=end_time,
            recurrence=recurrence
        )

        # Convert event.date to a proper date object if needed
        if isinstance(event.date, str):
            event_date = datetime.strptime(event.date, "%Y-%m-%d").date()
        else:
            event_date = event.date

        # Create recurring instances if recurrence is set
        if recurrence in ["daily", "weekly", "monthly"]:
            for i in range(1, 5):  # Create 5 future instances
                if recurrence == "daily":
                    new_date = event_date + timedelta(days=i)
                elif recurrence == "weekly":
                    new_date = event_date + timedelta(weeks=i)
                elif recurrence == "monthly":
                    try:
                        new_date = event_date + relativedelta(months=i)
                    except ValueError:  # Handles cases where a day doesn’t exist in that month (e.g., Feb 30)
                        new_date = event_date.replace(day=28) + relativedelta(months=i)  # Fallback to 28th


                Event.objects.create(
                    title=event.title, 
                    description=event.description,
                    date=new_date,
                    start_time=event.start_time,
                    end_time=event.end_time,
                    recurrence=recurrence
                )

        return redirect("events")



@csrf_exempt
def delete_event(request, event_id):
    if request.method == "DELETE":
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({"message": "Event deleted successfully!"})
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)





