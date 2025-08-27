import logging
from datetime import datetime
from functools import wraps

from django.conf import settings
from django.http import JsonResponse

from bookings.models import Table, TimeSlot, SlotAvailability

logger = logging.getLogger(__name__)


def get_adjacent_slots(time_slots, target_slot):
    index = next((i for i, ts in enumerate(time_slots) if ts.id == target_slot.id), None)
    if index is None:
        return []
    return list(filter(None, [
        time_slots[index - 1] if index > 0 else None,
        target_slot,
        time_slots[index + 1] if index + 1 < len(time_slots) else None
    ]))


def get_selected_date(request):
    date = request.GET.get("date")
    if not date:
        raise ValueError("Date is required")
    return date


def get_private_table_ids():
    return Table.objects.filter(private_hire=True).values_list("id", flat=True)


def get_ordered_timeslots():
    return TimeSlot.objects.order_by("timeslot")


def json_matrix_response(date, matrix):
    return JsonResponse({"date": date, "matrix": matrix})


def parse_date_string(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format")


def parse_time_string(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")


def handle_json_errors(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)
    return wrapper


def serialize_booking(booking):
    return {
        "id": booking.id,
        "table_id": booking.table.id,
        "table_name": str(booking.table),
        "name": booking.name,
        "email": booking.email,
        "phone": booking.phone,
        "paid": booking.paid,
        "notes": booking.notes,
    }


def set_slot_block(date, time_obj, is_blocked):
    timeslot = TimeSlot.objects.filter(timeslot=time_obj).first()
    if not timeslot:
        logger.warning(f"No TimeSlot found for time: {time_obj}")
        raise ValueError(f"No TimeSlot found for {time_obj}")

    availability, _ = SlotAvailability.objects.get_or_create(
        date=date,
        timeslot=timeslot,
        defaults={"seats_available": settings.DEFAULT_AVAILABLE_SEATS}
    )
    availability.is_blocked = is_blocked
    availability.save()


def summarize_availability(availabilities):
    return {
        "total_seats": sum(a.seats_available for a in availabilities) if availabilities.exists() else settings.DEFAULT_AVAILABLE_SEATS,
        "is_hired": any(a.is_blocked_for_hire for a in availabilities),
        "is_blocked": any(a.is_blocked for a in availabilities)
    }
