from django.shortcuts import render
from .models import ContactInfo

def contact_view(request):
    contact_info = ContactInfo.objects.all()
    return render(request, "contact/contact.html", {"contact_info": contact_info})

