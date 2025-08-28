from django.urls import path

from .views import (
    select_table,
    select_date_time,
    enter_details,
    confirm_booking,
    booking_success,
    booking_failure,
)

from .api_views import (
    get_available_times,
    get_booked_times,
    get_availability_matrix,
    bookings_for_date,
    apply_update_blocks,
)

from .admin_views import (
    booking_availability,
    view_bookings,
)

app_name = "bookings"

urlpatterns = [
    # Booking flow
    path("select-table/", select_table, name="select_table"),
    path("select-date-time/", select_date_time, name="select_date_time"),
    path("enter-details/", enter_details, name="enter_details"),
    path("confirm-booking/", confirm_booking, name="confirm_booking"),
    path("bookings-success/", booking_success, name="booking_success"),
    path("bookings-failure/", booking_failure, name="booking_failure"),

    # API endpoints
    path("get_available_times/", get_available_times, name="get_available_times"),
    path("get_booked_times/", get_booked_times, name="get_booked_times"),
    path("availability_matrix/", get_availability_matrix, name="availability_matrix"),
    path("bookings_by_date/", bookings_for_date, name="bookings_by_date"),
    path("apply_update_blocks/", apply_update_blocks, name="apply_update_blocks"),

    # Admin views
    path("booking_availability/", booking_availability, name="booking_availability"),
    path("view_bookings/", view_bookings, name="view_bookings"),
]


