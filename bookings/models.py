from django.core.exceptions import ValidationError
from django.db import models

class Table(models.Model):

    table_type = models.CharField(max_length=20, choices=[
        ('table_4', 'Table for up to 4'),
        ('table_8', 'Table for up to 8'),
        ('private_room', 'Private Hire Room (10 people)')
    ], unique=True)
    
    name = models.CharField(max_length=100, default="Unnamed Table")
    amount_of_time_hours = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

class TimeSlot(models.Model):
    timeslot = models.TimeField(blank=False, null=False)

class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('table', 'timeslot', 'date')  # Prevents double bookings
