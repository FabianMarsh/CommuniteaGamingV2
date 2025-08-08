from .models import Table, TimeSlot, Booking, SlotAvailability
from django.db import transaction
from django.core.exceptions import ValidationError
from .forms import BookingDetailsForm
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime, date
from django.contrib import messages
from django.db.models import Sum, Q
from decimal import Decimal
from django.core.mail import send_mail, get_connection
from .services import update_block, update_seats

import json
import logging

logger = logging.getLogger(__name__)

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


def select_date_time(request):
    if request.method == "POST":
        selected_date = request.POST.get("date")
        selected_time = request.POST.get("time")

        if selected_date and selected_time:
            request.session["selected_date"] = selected_date
            request.session["selected_time"] = selected_time
            return redirect("bookings:enter_details")

    selected_date = request.GET.get("date")
    selected_table = request.session.get("selected_table")
    selected_table_seats = selected_table.get("seats_required", 0) if selected_table else 0
    is_private = selected_table.get("private_hire") in [True, "True", 1, "1"] if selected_table else False

    available_times = []

    if selected_date:
        time_slots = TimeSlot.objects.order_by("timeslot")

        for slot in time_slots:
            availability = SlotAvailability.objects.filter(
                date=selected_date,
                timeslot=slot
            ).first()

            if not availability:
                continue  # No slot data yet—skip

            # Check for blocked slots and minimum seat availability
            if is_private:
                if not availability.is_blocked_for_hire:
                    continue
            elif availability.seats_available < selected_table_seats:
                continue

            available_times.append(slot.timeslot.strftime("%H:%M"))

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


def enter_details(request):
    if request.method == "POST":
        form = BookingDetailsForm(request.POST)
        if form.is_valid():
            request.session["user_data"] = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "phone": form.cleaned_data["phone"]
            }

            return redirect("bookings:confirm_booking")
    else:
        form = BookingDetailsForm()

    return render(request, "bookings/enter_details.html", {"form": form})


def confirm_booking(request):
    selected_table = request.session.get("selected_table")
    selected_time_id = request.session.get("selected_time")
    selected_date = request.session.get("selected_date")
    user_data = request.session.get("user_data")

    if not selected_table or not selected_time_id:
        return redirect("bookings:select_table")

    try:
        selected_time_slot = TimeSlot.objects.get(timeslot=selected_time_id)
        is_private = selected_table.get("private_hire") in [True, "True", 1, "1"]
        seats_needed = selected_table.get("seats_required", 0)

        if request.method == "POST":
            table_id = selected_table["id"]

            # Create the booking
            new_booking = Booking.objects.create(
                table_id=table_id,
                timeslot_id=selected_time_slot.id,
                date=selected_date,
                name=user_data.get("name"),
                email=user_data.get("email"),
                phone=user_data.get("phone"),
            )
            print("adjusted booking")
            # Update availability
            if is_private:
                update_block(selected_date, selected_time_slot)
            else:
                update_seats(selected_date, selected_time_slot, seats_needed)

            request.session["booking_id"] = new_booking.id
            return redirect("bookings:booking_success")

        # Convert price from string to decimal safely
        price_str = selected_table['price']
        selected_table['price'] = Decimal(price_str)

        return render(request, "bookings/confirm_booking.html", {
            "selected_table": selected_table,
            "selected_time_slot": selected_time_slot,
            "selected_date": selected_date,
            "user_data": user_data
        })

    except Exception as e:
        logger.error(f"Booking failed: {e}", exc_info=True)
        return redirect("bookings:booking_failure")


def booking_success(request):
    booking_id = request.session.get("booking_id")
    if not booking_id:
        return redirect("bookings:select_table")

    booking = Booking.objects.get(id=booking_id)

    # email = request.session["booking_email"] = booking.email
    selected_table = request.session.get("selected_table")
    price = Decimal(selected_table["price"]).quantize(Decimal('0.01'))

    # subject = "Your Booking Confirmation"
    # message = (
    # f"Hi!\n\n"
    # f"Your booking for table '{booking.table.name}' on {booking.date} "
    # f"at {booking.timeslot.timeslot} has been confirmed.\n\n"
# )

    # Include SumUp payment link if price > 0
    # if price > 0:
    #     message += (
    #         f"A payment of £{price:.2f} is required.\n"
    #         f"You can pay securely via SumUp here: https://pay.sumup.com/b2c/QKWSCH28\n\n"
    #     )

    # message += f"Thanks for choosing to hang with CommuniTea Gaming!"

    # recipient = email
    # sender = settings.EMAIL_HOST_USER

    # send_mail(subject, message, sender, [recipient], fail_silently=False, connection=get_connection(timeout=10))

    request.session.flush()

    return render(request, "bookings/booking_success.html", {
        "table_name": booking.table.name,
        "booking_date": booking.date,
        "timeslot": booking.timeslot.timeslot,
        "price": price,
    })


def booking_failure(request):

    return render(request, "bookings/booking_failure.html")

