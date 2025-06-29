from django.contrib import admin
from .models import Table, TimeSlot, Booking
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


