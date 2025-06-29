from django.urls import path
from .views import select_table, select_date, select_time, select_date_time, enter_details, confirm_booking, booking_success, get_available_times, get_booked_times

app_name = "bookings"

urlpatterns = [
    path("select-table/", select_table, name="select_table"),
    path("select-date/", select_date, name="select_date"),
    path("select-time/", select_time, name="select_time"),
    path("select-date-time/", select_date_time, name="select_date_time"),
    path("enter-details/", enter_details, name="enter_details"),
    path("confirm-booking/", confirm_booking, name="confirm_booking"),
    path("bookings-success/", booking_success, name="booking_success"),
    path("get_available_times/", get_available_times, name="get_available_times"),
    path("get_booked_times/", get_booked_times, name="get_booked_times"),
]
