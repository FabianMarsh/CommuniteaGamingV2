from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
import logging

from bookings.models import Booking, Table, TimeSlot, SlotAvailability
from bookings.services import get_slot_availability_for_date


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

    session_data = request.session.get("selected_table") or {}
    results = get_slot_availability_for_date(selected_date, session_data)

    return JsonResponse({"times": results})

def get_availability_matrix(request):
    try:
        selected_date = request.GET.get("date")
        if not selected_date:
            return JsonResponse({"error": "Date is required"}, status=400)

        time_slots = TimeSlot.objects.order_by("timeslot")
        matrix = []

        for slot in time_slots:
            availabilities = SlotAvailability.objects.filter(
                date=selected_date,
                timeslot=slot
            )

            availabilities = SlotAvailability.objects.filter(date=selected_date, timeslot=slot)

            if availabilities.exists():
                total_seats = sum(a.seats_available for a in availabilities)
            else:
                total_seats = settings.DEFAULT_AVAILABLE_SEATS

            is_hired = any(a.is_blocked_for_hire for a in availabilities)
            is_blocked = any(a.is_blocked for a in availabilities)

            matrix.append({
                "time": str(slot.timeslot),
                "available_seats": total_seats,
                "is_hired": is_hired,
                "is_blocked": is_blocked
            })

        return JsonResponse({
            "date": selected_date,
            "matrix": matrix
        })

    except Exception as e:
        logger.error(f"Error in availability view: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@require_GET
def bookings_for_date(request):
    try:
        selected_date = request.GET.get("date")
        if not selected_date:
            return JsonResponse({"error": "Date is required"}, status=400)

        time_slots = TimeSlot.objects.order_by("timeslot")
        matrix = []

        for slot in time_slots:
            bookings = Booking.objects.filter(date=selected_date, timeslot=slot)

            slot_data = {
                "timeslot": str(slot.timeslot),  # e.g. "12:00:00"
                "bookings": [
                    {
                        "id": booking.id,
                        "table_id": booking.table.id,
                        "table_name": str(booking.table),
                        "name": booking.name,
                        "email": booking.email,
                        "phone": booking.phone,
                        "paid": booking.paid,
                        "notes": booking.notes,
                    }
                    for booking in bookings
                ]
            }

            matrix.append(slot_data)

        return JsonResponse({
            "date": selected_date,
            "matrix": matrix
        })

    except Exception as e:
        logger.error(f"Error in bookings view: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)
