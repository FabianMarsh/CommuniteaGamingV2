from django.shortcuts import render
from contact.models import ContactInfo


# Create your views here.

def index(request):
    """ A view to return the index page """
    contact_info = ContactInfo.objects.first()

    return render(request, "home/index.html", {"contact_info": contact_info})
