from django.db import transaction
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import SlotAvailability, TimeSlot, Booking, Table
from django.conf import settings
import logging
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

logger = logging.getLogger(__name__)


def update_seats(date, time_slot, seats_needed, delete=False):
    time_slots = list(TimeSlot.objects.order_by("timeslot"))
    current_index = next((i for i, ts in enumerate(time_slots) if ts.id == time_slot.id), None)

    if current_index is None:
        return

    relevant_slots = [
        time_slots[current_index - 1] if current_index > 0 else None,
        time_slot,
        time_slots[current_index + 1] if current_index + 1 < len(time_slots) else None
    ]

    with transaction.atomic():
        # slot = previous, current, next
        for slot in filter(None, relevant_slots):
            avail, _ = SlotAvailability.objects.get_or_create(
                date=date,
                timeslot=slot,

                defaults={"seats_available": settings.DEFAULT_AVAILABLE_SEATS}
            )
            if delete:
                avail.seats_available += seats_needed
            else:
                if avail.seats_available < seats_needed:
                    logger.warning(f"Attempted to subtract {seats_needed} seats, but only {avail.seats_available} available for slot {slot}")
                    raise ValidationError("Not enough seats available for this timeslot.")
                avail.seats_available -= seats_needed
            avail.save()



def update_block(date, time_slot, delete=False):
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
        if delete:
            availability.is_blocked_for_hire = False
        else:
            availability.is_blocked_for_hire = True

        availability.save()


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


def get_slot_availability_for_date(date, session_data=None):
    is_private = session_data.get("private_hire", False)
    selected_seats = session_data.get("seats_required", settings.DEFAULT_AVAILABLE_SEATS)

    time_slots = TimeSlot.objects.order_by("timeslot")
    results = []

    for slot in time_slots:
        # Get all availability records for this date and timeslot
        availabilities = SlotAvailability.objects.filter(date=date, timeslot=slot)

        total_seats = sum(a.seats_available for a in availabilities)
        is_hired = any(a.is_blocked_for_hire for a in availabilities)
        is_blocked = any(a.is_blocked for a in availabilities)

        if is_private and is_hired:
            continue
        
        if is_blocked:
            continue

        if not is_private or total_seats >= selected_seats:
            results.append({
                "time": str(slot.timeslot),
                "available_seats": total_seats,
                "is_hired": is_hired,
                "is_blocked": is_blocked
            })

    return results


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

            total_seats = sum(a.seats_available for a in availabilities)
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

@csrf_exempt
def update_slot_blocks(date_str, updates):
    if not date_str or not isinstance(updates, list):
        raise ValueError("Invalid input")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format")

    for item in updates:
        time_str = item.get("time")
        is_blocked = item.get("is_blocked", False)

        if not time_str:
            continue

        try:
            time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}")

        try:
            timeslot = TimeSlot.objects.get(timeslot=time_obj)
        except TimeSlot.DoesNotExist:
            raise ValueError(f"No TimeSlot found for {time_obj}")

        availability, _ = SlotAvailability.objects.get_or_create(
            date=date,
            timeslot=timeslot,
            defaults={"seats_available": settings.DEFAULT_AVAILABLE_SEATS}
        )
        availability.is_blocked = is_blocked
        availability.save()

