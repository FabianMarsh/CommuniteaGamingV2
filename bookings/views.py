from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Table, TimeSlot, Booking
from datetime import datetime


def select_table(request):
    if request.method == "POST":
        table_id = request.POST.get("table") 
        
        selected_table = Table.objects.get(id=table_id)

        request.session["selected_table"] = {
            "id": selected_table.id,
            "name": selected_table.name,
            "price": float(selected_table.price)
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

from django.shortcuts import render, redirect
from django.http import JsonResponse

def select_date_time(request):
    if request.method == "POST":
        selected_date = request.POST.get("date")  # ✅ Get selected date from form
        selected_time = request.POST.get("time")  # ✅ Get selected time from form

        if selected_date and selected_time:
            # ✅ Store selected values in session
            request.session["selected_date"] = selected_date
            request.session["selected_time"] = selected_time

            # ✅ Redirect to confirm booking page
            return redirect("bookings:confirm_booking")

    # ✅ If accessed via GET, ensure available times are ready for selection
    selected_date = request.GET.get("date")
    available_times = []

    if selected_date:
        booked_times = Booking.objects.filter(date=selected_date).values_list("timeslot_id", flat=True)
        all_times = TimeSlot.objects.values_list("timeslot", flat=True)
        available_times = TimeSlot.objects.exclude(id__in=booked_times).values_list("timeslot", flat=True)

    return render(request, "bookings/select_date_time.html", {
        "available_times": available_times,
        "selected_date": selected_date
    })


def get_available_times(request):
    available_times = TimeSlot.objects.values_list("timeslot", flat=True)  # ✅ Get all available slots
    return JsonResponse({"times": list(available_times)})  # ✅ Return unfiltered times



def get_booked_times(request):
    selected_date = request.GET.get("date")  # ✅ Get selected date

    if not selected_date:
        return JsonResponse({"error": "Date is required"}, status=400)  # ✅ Handle missing dates

    # ✅ Retrieve booked times as time strings (not IDs)
    booked_times = Booking.objects.filter(date=selected_date).values_list("timeslot__timeslot", flat=True)

    print("Booked TimeSlots (formatted):", list(booked_times))  # ✅ Debugging step

    return JsonResponse({"times": list(booked_times)})  # ✅ Send formatted time slots





def confirm_booking(request):
    selected_table = request.session.get("selected_table")
    selected_time_id = request.session.get("selected_time")
    selected_date = request.session.get("selected_date")

    if not selected_table or not selected_time_id:
        return redirect("bookings:select_table")  # Redirect if missing required data

    selected_time_slot = TimeSlot.objects.get(timeslot=selected_time_id)

    if request.method == "POST":        
        # Create booking entry in database
        new_booking = Booking.objects.create(
            table_id=selected_table["id"], 
            timeslot_id=selected_time_slot.id, 
            date=selected_date
        )

        request.session.flush()  # Clear session after storing booking
        request.session["booking_id"] = new_booking.id  # Store booking ID for success page

        return redirect("bookings:booking_success")  # Redirect to success page


    return render(request, "bookings/confirm_booking.html", {
        "selected_table": selected_table,
        "selected_time_slot": selected_time_slot,
        "selected_date": selected_date
    })

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

