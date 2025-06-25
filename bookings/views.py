from .models import Table, TimeSlot, Booking, SlotAvailability
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime, date
from django.contrib import messages
from django.db.models import Sum

import json

from django.conf import settings


def select_table(request):
    if request.method == "POST":
        table_id = request.POST.get("table") 
        
        selected_table = Table.objects.get(id=table_id)

        request.session["selected_table"] = {
            "id": selected_table.id,
            "name": selected_table.name,
            "price": float(selected_table.price),
            "seats_required": selected_table.seats_required,
            "private_hire": selected_table.private_hire
        }

        request.session["selected_table"]["price"] = "{:.2f}".format(request.session["selected_table"]["price"])

        request.session.modified = True
        return redirect("bookings:select_date_time")

    tables = Table.objects.all()
    return render(request, "bookings/select_table.html", {"tables": tables})



# old date and time view
def select_date(request):
    selected_table = request.session.get("selected_table")  # Get stored value

    if not selected_table:
        return redirect("bookings:select_table")

    if request.method == "POST":
        selected_date = request.POST.get("date") 
        request.session["selected_date"] = selected_date 
        request.session.modified = True
        return redirect("bookings:select_time") 

    return render(request, "bookings/select_date.html", {"selected_table": selected_table})
    

def select_time(request):
    selected_table = request.session.get("selected_table")

    if "selected_table" not in request.session:
        return redirect("bookings:select_table")
    elif "selected_date" not in request.session:
        return redirect("bookings:select_date")

    available_times = ["12:00", "14:00", "18:00"]  # Example times, replace with logic

    if request.method == "POST":
        selected_time = request.POST.get("time")
        request.session["selected_time"] = request.POST["time"]

        return redirect("bookings:confirm_booking")

    time_slots = TimeSlot.objects.all()
    return render(request, "bookings/select_time.html", {"time_slots": time_slots, "selected_table": selected_table})


# new date and time view

def select_date_time(request):
    if request.method == "POST":
        selected_date = request.POST.get("date")  
        selected_time = request.POST.get("time")  

        if selected_date and selected_time:
            request.session["selected_date"] = selected_date
            request.session["selected_time"] = selected_time
            return redirect("bookings:confirm_booking")

    selected_date = request.GET.get("date")
    available_times = []

    if selected_date:
        booked_times = Booking.objects.filter(date=selected_date).values_list("timeslot_id", flat=True)
        all_times = TimeSlot.objects.values_list("timeslot", flat=True)
        available_times = TimeSlot.objects.exclude(id__in=booked_times).values_list("timeslot", flat=True)

    selected_table = request.session.get("selected_table")
    selected_table_seats = selected_table.get("seats_required") or 0 if selected_table else 0

    return render(request, "bookings/select_date_time.html", {
        "available_times": available_times,
        "selected_date": selected_date,
        "selected_table_seats": selected_table_seats,
    })


def get_booked_times(request):
    selected_date = request.GET.get("date")
    if not selected_date:
        return JsonResponse({"error": "Date is required"}, status=400)

    selected_table = request.session.get("selected_table")
    is_private = selected_table and selected_table.get("private_hire") in [True, "True", 1, "1"]

    if is_private:
        private_table_ids = Table.objects.filter(private_hire=True).values_list("id", flat=True)
        booked = Booking.objects.filter(date=selected_date, table_id__in=private_table_ids)
    else:
        private_table_ids = Table.objects.filter(private_hire=True).values_list("id", flat=True)
        booked = Booking.objects.exclude(table_id__in=private_table_ids).filter(date=selected_date)

    booked_times = booked.values_list("timeslot__timeslot", flat=True)

    return JsonResponse({"times": list(booked_times)})

def get_available_times(request):
    selected_date = request.GET.get("date")
    if not selected_date:
        return JsonResponse({"error": "No date provided."}, status=400)

    selected_table = request.session.get("selected_table") or {}
    is_private = selected_table.get("private_hire", False)
    selected_seats = selected_table.get("seats_required", 0)

    time_slots = TimeSlot.objects.order_by("timeslot")
    response_data = {"times": []}

    for slot in time_slots:
        availability, _ = SlotAvailability.objects.get_or_create(
            date=selected_date,
            timeslot=slot,
            defaults={"seats_available": 68}
        )

        # Step 2 — hide blocked slots from non-private-hire bookings
        if is_private and availability.is_blocked_for_hire:
            continue

        if not is_private or availability.seats_available >= selected_seats:
            response_data["times"].append({
                "time": str(slot.timeslot),
                "available_seats": availability.seats_available
            })

    return JsonResponse(response_data)


def confirm_booking(request):
    selected_table = request.session.get("selected_table")
    selected_time_id = request.session.get("selected_time")
    selected_date = request.session.get("selected_date")

    if not selected_table or not selected_time_id:
        return redirect("bookings:select_table")

    selected_time_slot = TimeSlot.objects.get(timeslot=selected_time_id)
    is_private = selected_table.get("private_hire") in [True, "True", 1, "1"]
    seats_needed = selected_table.get("seats_required", 0)

    if request.method == "POST":
        table_id = selected_table["id"]
        is_private = selected_table.get("private_hire") in [True, "True", 1, "1"]
        seats_needed = selected_table.get("seats_required", 0)

        # Create the booking
        new_booking = Booking.objects.create(
            table_id=table_id,
            timeslot_id=selected_time_slot.id,
            date=selected_date
        )

        if is_private:
            update_block(selected_date, selected_time_slot)
        else:
            update_seats(selected_date, selected_time_slot, seats_needed)

        request.session.flush()
        request.session["booking_id"] = new_booking.id
        return redirect("bookings:booking_success")


    return render(request, "bookings/confirm_booking.html", {
        "selected_table": selected_table,
        "selected_time_slot": selected_time_slot,
        "selected_date": selected_date
    })


def update_seats(date, time_slot, seats_needed):
    time_slots = list(TimeSlot.objects.order_by("timeslot"))
    current_index = next((i for i, ts in enumerate(time_slots) if ts.id == time_slot.id), None)

    if current_index is None:
        return

    relevant_slots = [
        time_slots[current_index - 1] if current_index > 0 else None,
        time_slot,
        time_slots[current_index + 1] if current_index + 1 < len(time_slots) else None
    ]

    for slot in filter(None, relevant_slots):
        avail, _ = SlotAvailability.objects.get_or_create(
            date=date,
            timeslot=slot,
            defaults={"seats_available": settings.DEFAULT_AVAILABLE_SEATS}
        )
        avail.seats_available -= seats_needed
        avail.save()


def update_block(date, time_slot):
    time_slots = list(TimeSlot.objects.order_by("timeslot"))
    current_index = next((i for i, ts in enumerate(time_slots) if ts.id == time_slot.id), None)

    if current_index is None:
        return

    affected_slots = [
        time_slots[current_index - 1] if current_index > 0 else None,
        time_slot,
        time_slots[current_index + 1] if current_index + 1 < len(time_slots) else None
    ]

    for slot in filter(None, affected_slots):
        availability, _ = SlotAvailability.objects.get_or_create(
            date=date,
            timeslot=slot,
            defaults={"seats_available": settings.DEFAULT_AVAILABLE_SEATS}
        )
        availability.is_blocked_for_hire = True
        availability.save()



def booking_success(request):
    booking_id = request.session.get("booking_id")  # Retrieve the latest booking
    if not booking_id:
        return redirect("bookings:select_table")  # Redirect if no booking exists

    booking = Booking.objects.get(id=booking_id)

    return render(request, "bookings/booking_success.html", {
        "table_name": booking.table.name,
        "booking_date": booking.date,
        "timeslot": booking.timeslot.timeslot,
    })


