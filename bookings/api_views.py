from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
import logging

from bookings.models import Booking, TimeSlot, SlotAvailability
from bookings.services import get_slot_availability_for_date, build_availability_matrix
from bookings.utils.helpers import (
    get_selected_date,
    get_private_table_ids,
    serialize_booking,
    safe_json_view,
    json_matrix_response
)

logger = logging.getLogger(__name__)


@require_GET
@safe_json_view
def get_booked_times(request):
    selected_date = get_selected_date(request)
    selected_table = request.session.get("selected_table") or {}
    is_private = selected_table.get("private_hire") in [True, "True", 1, "1"]

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
@safe_json_view
def get_available_times(request):
    selected_date = get_selected_date(request)
    session_data = request.session.get("selected_table") or {}
    results = get_slot_availability_for_date(selected_date, session_data)
    return JsonResponse({"times": results})


@require_GET
@safe_json_view
def get_availability_matrix(request):
    selected_date = get_selected_date(request)
    matrix = build_availability_matrix(selected_date)
    return json_matrix_response(selected_date, matrix)


@require_GET
@safe_json_view
def bookings_for_date(request):
    selected_date = get_selected_date(request)
    matrix = []

    for slot in TimeSlot.objects.order_by("timeslot"):
        bookings = Booking.objects.filter(date=selected_date, timeslot=slot)
        matrix.append({
            "timeslot": str(slot.timeslot),
            "bookings": [serialize_booking(b) for b in bookings]
        })

    return json_matrix_response(selected_date, matrix)
