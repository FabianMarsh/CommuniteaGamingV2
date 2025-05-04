from django.shortcuts import render
from .models import Table, TimeSlot

# Create your views here.

from django.shortcuts import render, redirect
from .models import Table, TimeSlot
from datetime import datetime

def select_table(request):
    tables = Table.objects.all()

    if request.method == "POST":
        request.session["selected_table"] = request.POST["table"]
        return redirect("bookings:select_date")
    
    return render(request, "bookings/select_table.html", {"tables": tables})

def select_date(request):
    if "selected_table" not in request.session:
        return redirect("bookings:select_table")

    if request.method == "POST":
        request.session["selected_table"] = request.POST.get("table")
        return redirect("bookings:select_time")

    return render(request, "bookings/select_date.html")
    
    return render(request, "bookings/select_date.html")

def select_time(request):
    if "selected_date" not in request.session:
        return redirect("bookings:select_date")

    available_times = ["12:00", "14:00", "18:00"]  # Example times, replace with logic
    if request.method == "POST":
        request.session["selected_time"] = request.POST["time"]
        return redirect("bookings:confirm_booking")

    return render(request, "bookings/select_time.html", {"times": available_times})

def confirm_booking(request):
    if "selected_table" not in request.session or "selected_time" not in request.session:
        return redirect("bookings:select_table")

    table = request.session["selected_table"]
    date = request.session["selected_date"]
    time = request.session["selected_time"]

    # Check if the time slot is already booked
    existing_booking = TimeSlot.objects.filter(table=table, date=date, time=time).exists()

    if existing_booking:
        messages.error(request, "This time slot is already booked. Please select a different time.")
        return redirect("select_time")

    if request.method == "POST":
        TimeSlot.objects.create(
            table=table,
            date=date,
            time=time,
            user=request.user
        )
        return redirect("bookings:booking_success")

    return render(request, "bookings/confirm_booking.html")

