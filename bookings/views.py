import logging

from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect

from .models import Table, TimeSlot, Booking, SlotAvailability
from .forms import BookingDetailsForm
from .services import update_block, update_seats
from .utils.helpers import safe_decimal, get_booking_session_data, is_private_hire

logger = logging.getLogger(__name__)


def select_table(request):
    if request.method == "POST":
        table_id = request.POST.get("table")
        selected_table = Table.objects.get(id=table_id)

        request.session["selected_table"] = {
            "id": selected_table.id,
            "name": selected_table.name,
            "price": "{:.2f}".format(float(selected_table.price)),
            "seats_required": selected_table.seats_required,
            "private_hire": selected_table.private_hire,
        }

        request.session.modified = True
        return redirect("bookings:select_date_time")

    tables = Table.objects.all()
    return render(request, "bookings/select-table.html", {"tables": tables})


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
    is_private = is_private_hire(selected_table)

    available_times = []

    if selected_date:
        time_slots = get_ordered_timeslots()
        for slot in time_slots:
            availability = SlotAvailability.objects.filter(date=selected_date, timeslot=slot).first()
            if not availability:
                continue
            if is_private and not availability.is_blocked_for_hire:
                continue
            if not is_private and availability.seats_available < selected_table_seats:
                continue
            available_times.append(slot.timeslot.strftime("%H:%M"))

    return render(request, "bookings/select-date-time.html", {
        "available_times": available_times,
        "selected_date": selected_date,
        "selected_table_seats": selected_table_seats,
    })


def enter_details(request):
    if request.method == "POST":
        form = BookingDetailsForm(request.POST)
        if form.is_valid():
            request.session["user_data"] = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "phone": form.cleaned_data["phone"],
                "notes": form.cleaned_data["notes"],
            }
            return redirect("bookings:confirm_booking")
    else:
        form = BookingDetailsForm()

    return render(request, "bookings/enter-details.html", {"form": form})


def confirm_booking(request):
    selected_table, selected_time_id, selected_date, user_data = get_booking_session_data(request.session)

    if not selected_table or not selected_time_id or not user_data:
        logger.warning("Missing session data for booking")
        return redirect("bookings:select_table")

    try:
        selected_time_slot = TimeSlot.objects.get(timeslot=selected_time_id)
        is_private = selected_table.get("private_hire") in [True, "True", 1, "1"]
        seats_needed = selected_table.get("seats_required", 0)

        if request.method == "POST":
            try:
                with transaction.atomic():
                    table_id = selected_table["id"]
                    logger.info(
                        f"Booking attempt: table={table_id}, time={selected_time_slot.id}, "
                        f"date={selected_date}, private={is_private}, seats={seats_needed}"
                    )

                    new_booking = Booking.objects.create(
                        table_id=table_id,
                        timeslot_id=selected_time_slot.id,
                        date=selected_date,
                        name=user_data.get("name"),
                        email=user_data.get("email"),
                        phone=user_data.get("phone"),
                        notes=user_data.get("notes"),
                    )

                    if is_private:
                        update_block(selected_date, selected_time_slot)
                    else:
                        update_seats(selected_date, selected_time_slot, seats_needed)

                    request.session["booking_id"] = new_booking.id
                    return redirect("bookings:booking_success")

            except Exception as e:
                logger.error(f"Booking transaction failed: {e}", exc_info=True)
                return redirect("bookings:booking_failure")

        selected_table["price"] = safe_decimal(selected_table.get("price"))

        return render(request, "bookings/confirm-booking.html", {
            "selected_table": selected_table,
            "selected_time_slot": selected_time_slot,
            "selected_date": selected_date,
            "user_data": user_data,
        })

    except TimeSlot.DoesNotExist:
        logger.error(f"TimeSlot not found for ID: {selected_time_id}")
        return redirect("bookings:booking_failure")
    except Exception as e:
        logger.error(f"Booking view failed: {e}", exc_info=True)
        return redirect("bookings:booking_failure")


def booking_success(request):
    booking_id = request.session.get("booking_id")
    if not booking_id:
        return redirect("bookings:select_table")

    booking = Booking.objects.get(id=booking_id)
    selected_table = request.session.get("selected_table")
    price = safe_decimal(selected_table.get("price")).quantize(Decimal("0.01"))

    request.session.flush()

    return render(request, "bookings/booking-success.html", {
        "table_name": booking.table.name,
        "booking_date": booking.date,
        "timeslot": booking.timeslot.timeslot,
        "price": price,
    })


def booking_failure(request):
    return render(request, "bookings/booking-failure.html")
