from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "start_time")  # Show these fields in the admin list
    search_fields = ("title", "description")  # Enable search functionality
    ordering = ("date", "start_time")  # Sort by date & time


