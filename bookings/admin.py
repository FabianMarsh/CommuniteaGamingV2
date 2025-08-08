from django.core.exceptions import ValidationError
from django.contrib import admin, messages
from django.db import transaction
from .models import Table, TimeSlot, Booking
from .services import update_block, update_seats
from datetime import date, timedelta

# Register your models here.

class TableAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "table_type",
        "amount_of_time_hours",
        "price",
        "seats_required",
        "private_hire",
    )

admin.site.register(Table, TableAdmin)

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TimeSlot._meta.fields]

    ordering = ['timeslot'] # Ensure sorting in the admin panel

admin.site.register(TimeSlot, TimeSlotAdmin)

class ThisWeekFilter(admin.SimpleListFilter):
    title = "This Week"
    parameter_name = "this_week"

    def lookups(self, request, model_admin):
        return (
            ("yes", "This Week"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())  # Monday
            end_of_week = start_of_week + timedelta(days=6)          # Sunday
            return queryset.filter(date__range=(start_of_week, end_of_week))
        return queryset

class NextWeekFilter(admin.SimpleListFilter):
    title = "Next Week"
    parameter_name = "next_week"

    def lookups(self, request, model_admin):
        return (("yes", "Next Week"),)

    def queryset(self, request, queryset):
        if self.value() == "yes":
            today = date.today()
            start_of_next_week = today - timedelta(days=today.weekday()) + timedelta(days=7)  # Next Monday
            end_of_next_week = start_of_next_week + timedelta(days=6)  # Next Sunday
            return queryset.filter(date__range=(start_of_next_week, end_of_next_week))
        return queryset


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_date",
        "table_name",
        "time_slot",
        "name",
        "email",
        "phone",
        "paid_status"
    )

    list_filter = ("date", "timeslot", ThisWeekFilter, NextWeekFilter)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        try:
            if obj.table.private_hire:
                update_block(obj.date, obj.timeslot)
                messages.success(request, "Private hire block applied.")
            else:
                update_seats(obj.date, obj.timeslot, obj.table.seats_required)
                messages.success(request, f"{obj.table.seats_required} seats allocated.")
        except ValidationError as e:
            messages.error(request, f"Seat allocation failed: {e}")

    def delete_model(self, request, obj):
        with transaction.atomic():
            try:
                if obj.table.private_hire:
                    update_block(obj.date, obj.timeslot, delete=True)
                    messages.success(request, "Private hire block removed.")
                else:
                    update_seats(obj.date, obj.timeslot, obj.table.seats_required, delete=True)
                    messages.success(request, f"{obj.table.seats_required} seats restored.")
            except ValidationError as e:
                messages.error(request, f"Seat restoration failed: {e}")

        super().delete_model(request, obj)


    def table_name(self, obj):
        return obj.table.name

    def booking_date(self, obj):
        return obj.date

    def time_slot(self, obj):
        return f"{obj.timeslot.timeslot}"

    def paid_status(self, obj):
        return "Paid" if obj.paid else "Unpaid"

    paid_status.short_description = "Payment"

admin.site.register(Booking, BookingAdmin)


