from django.urls import path
from .views import select_table, select_date, select_time, confirm_booking

app_name = "bookings"

urlpatterns = [
    path("select-table/", select_table, name="select_table"),
    path("select-date/", select_date, name="select_date"),
    path("select-time/", select_time, name="select_time"),
    path("confirm-booking/", confirm_booking, name="confirm_booking"),
]
