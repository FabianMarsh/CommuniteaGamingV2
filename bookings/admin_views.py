from django.shortcuts import render, redirect

def booking_availability(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "bookings/booking-availability.html")
    else:
        return redirect("bookings:select_table")

def view_bookings(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "bookings/view-bookings.html")
    else:
        return redirect("bookings:select_table")