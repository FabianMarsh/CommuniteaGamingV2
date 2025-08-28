from django.http import JsonResponse
from datetime import datetime

def is_admin(request):
    is_admin = request.user.is_authenticated and request.user.is_staff
    return JsonResponse({ "is_admin": is_admin })

def parse_date_string(date_str):
    """Convert a YYYY-MM-DD string to a date object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")