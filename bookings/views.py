from .models import Table, TimeSlot, Booking, SlotAvailability
from .forms import BookingDetailsForm
from django.shortcuts import render, redirect
from datetime import date
from django.db.models import Sum, Q
from django.db import transaction
from decimal import Decimal
from django.core.mail import send_mail, get_connection
from .services import update_block, update_seats, get_available_times, get_booked_times, update_slot_blocks
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

        # Convert price from string to Decimal safely
        try:
            selected_table["price"] = Decimal(selected_table["price"])
        except (KeyError, ValueError, TypeError) as e:
            logger.warning(f"Price conversion failed: {e}")
            selected_table["price"] = Decimal("0.00")

        return render(request, "bookings/confirm_booking.html", {
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

@csrf_exempt
@require_POST
def update_blocks(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    date = data.get("date")
    updates = data.get("updates", [])

    try:
        update_slot_blocks(date, updates)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"status": "success"})

# Admin views

def booking_availability(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "bookings/booking_availability.html")
    else:
        return redirect("bookings:select_table")

def view_bookings(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "bookings/view_bookings.html")
    else:
        return redirect("bookings:select_table")



