from django.contrib import admin
from .models import Table, TimeSlot, Booking

# Register your models here.
admin.site.register(Table)
admin.site.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',) # Show time field in the admin list

    ordering = ['time'] # Ensure sorting in the admin panel

admin.site.register(Booking)