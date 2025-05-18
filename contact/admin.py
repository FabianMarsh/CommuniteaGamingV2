from django.contrib import admin
from .models import ContactInfo

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number")

