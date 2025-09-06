import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from bookings.models import Booking, TimeSlot
from bookings.services import (
    get_slot_availability_for_date,
    build_availability_matrix,
    apply_slot_blocks,
)
from bookings.utils.helpers import (
    get_selected_date,
    get_private_table_ids,
    serialize_booking,
    handle_json_errors,
    json_matrix_response,
    get_ordered_timeslots,
    is_private_hire
)

logger = logging.getLogger(__name__)


@require_GET
@handle_json_errors
def get_booked_times(request):
    selected_date = get_selected_date(request)
    selected_table = request.session.get("selected_table") or {}
    is_private = is_private_hire(selected_table)

    logger.debug(f"Session data: {selected_table}")
    logger.debug(f"Selected date: {selected_date}")

    private_table_ids = get_private_table_ids()

    if is_private:
        booked = Booking.objects.filter(date=selected_date, table_id__in=private_table_ids)
    else:
        booked = Booking.objects.exclude(table_id__in=private_table_ids).filter(date=selected_date)

    booked_times = booked.values_list("timeslot__timeslot", flat=True)
    return JsonResponse({"times": list(booked_times)})


@require_GET
@handle_json_errors
def get_available_times(request):
    selected_date = get_selected_date(request)
    session_data = request.session.get("selected_table") or {}
    results = get_slot_availability_for_date(selected_date, session_data) or []
    return JsonResponse({"times": results})


@require_GET
@handle_json_errors
def get_availability_matrix(request):
    selected_date = get_selected_date(request)
    matrix = build_availability_matrix(selected_date)
    return json_matrix_response(selected_date, matrix)


@require_GET
@handle_json_errors
def bookings_for_date(request):
    selected_date = get_selected_date(request)
    matrix = []

    for slot in get_ordered_timeslots():
        bookings = Booking.objects.filter(date=selected_date, timeslot=slot)
        matrix.append({
            "timeslot": str(slot.timeslot),
            "bookings": [serialize_booking(b) for b in bookings]
        })

    return json_matrix_response(selected_date, matrix)


@csrf_exempt
@require_POST
@handle_json_errors
def apply_update_blocks(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON payload")

    logger.debug(f"Received block update request: {data}")

    date = data.get("date")
    updates = data.get("updates", [])

    if not date:
        raise ValueError("Missing 'date' in payload")

    apply_slot_blocks(date, updates)
    return JsonResponse({"status": "success"})

