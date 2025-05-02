from django.shortcuts import render
from .models import Table, TimeSlot

# Create your views here.

def bookings(request):
    """ A view to return the bookings page """

    tables = Table.objects.all()
    times = TimeSlot.objects.all()

    context = {
        'tables': tables,
        'times': times,
    }

    return render(request, 'bookings/bookings.html', context)