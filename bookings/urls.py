from django.urls import path
from .views import select_table, select_date, select_time, select_date_time, confirm_booking, booking_success, get_available_times

app_name = "bookings"

urlpatterns = [
    path("select-table/", select_table, name="select_table"),
    path("select-date/", select_date, name="select_date"),
    path("select-time/", select_time, name="select_time"),
    path("select-date-time/", select_date_time, name="select_date_time"),
    path("confirm-booking/", confirm_booking, name="confirm_booking"),
    path("bookings-success/", booking_success, name="booking_success"),
    path("get_available_times/<str:selected_date>/", get_available_times, name="get_available_times"),

]
