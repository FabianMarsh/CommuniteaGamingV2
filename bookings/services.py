import logging
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse

from .models import SlotAvailability, TimeSlot
from bookings.utils.helpers import (
    format_slot_summary,
    get_adjacent_slots,
    get_ordered_timeslots,
    parse_date_string,
    parse_time_string,
    set_slot_block,
    summarize_availability,
    is_private_hire
)

logger = logging.getLogger(__name__)


def update_seats(date, time_slot, seats_needed, delete=False):
    time_slots = list(get_ordered_timeslots())
    relevant_slots = get_adjacent_slots(time_slots, time_slot)

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
    time_slots = list(get_ordered_timeslots())
    relevant_slots = get_adjacent_slots(time_slots, time_slot)

    with transaction.atomic():
        for slot in filter(None, relevant_slots):
            availability, _ = SlotAvailability.objects.get_or_create(
                date=date,
                timeslot=slot,

                defaults={"seats_available": settings.DEFAULT_AVAILABLE_SEATS}
            )
            availability.is_blocked_for_hire = not delete
            availability.save()


def get_slot_availability_for_date(date, session_data=None):
    session_data = session_data or {}
    is_private = is_private_hire(session_data)
    selected_seats = session_data.get("seats_required", settings.DEFAULT_AVAILABLE_SEATS)

    time_slots = get_ordered_timeslots()
    results = []
    logger.debug(f"Session data in get_available_times: {session_data}")

    for slot in time_slots:
        # Get all availability records for this date and timeslot
        availabilities = SlotAvailability.objects.filter(date=date, timeslot=slot)
        
        summary = summarize_availability(availabilities)

        if is_private and summary["is_hired"]:
            continue
        
        if summary["is_blocked"]:
            continue

        if not is_private or summary["total_seats"] >= selected_seats:
            results.append(format_slot_summary(slot, summary))

    return results or []


def build_availability_matrix(date):
    matrix = []
    for slot in get_ordered_timeslots():
        availabilities = SlotAvailability.objects.filter(date=date, timeslot=slot)
        summary = summarize_availability(availabilities)

        matrix.append(format_slot_summary(slot, summary))

    return matrix


def apply_slot_blocks(date_str, updates):
    if not date_str or not isinstance(updates, list):
        raise ValueError("Invalid input")

    date = parse_date_string(date_str)

    for item in updates:
        time_str = item.get("time")
        is_blocked = item.get("is_blocked", False)

        if not time_str:
            continue

        time_obj = parse_time_string(time_str)
        set_slot_block(date, time_obj, is_blocked)