from django.contrib import admin
from .models import Table, TimeSlot, Booking

# Register your models here.
admin.site.register(Table)
admin.site.register(TimeSlot)
admin.site.register(Booking)