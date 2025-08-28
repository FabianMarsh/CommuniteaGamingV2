from django.shortcuts import render
from contact.models import ContactInfo


# Create your views here.

def index(request):
    contact_info = ContactInfo.objects.first()

    return render(request, "home/index.html", {"contact_info": contact_info})
