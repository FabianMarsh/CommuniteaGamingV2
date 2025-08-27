from functools import wraps
from django.http import JsonResponse
import logging
from bookings.models import Table, TimeSlot

logger = logging.getLogger(__name__)

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

def safe_json_view(view_func):
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
