from django.contrib import admin
from .models import Table, TimeSlot, Booking

# Register your models here.
admin.site.register(Table)
admin.site.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',) # Show time field in the admin list

    ordering = ['time'] # Ensure sorting in the admin panel

class BookingAdmin(admin.ModelAdmin):
    list_display = ("table_name", "booking_date", "time_slot")

    def table_name(self, obj):
        return obj.table.name  # Shows table name

    def booking_date(self, obj):
        return obj.date  # Shows booking date

    def time_slot(self, obj):
        return f"{obj.timeslot.start_time} - {obj.timeslot.end_time}"  # Shows time slot

admin.site.register(Booking, BookingAdmin)
