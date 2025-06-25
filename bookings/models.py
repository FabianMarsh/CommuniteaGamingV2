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
    seats_required = models.PositiveIntegerField(default=0)
    private_hire = models.BooleanField(default=False)

class TimeSlot(models.Model):
    timeslot = models.TimeField(blank=False, null=False)

    def __str__(self):
        return f"{self.timeslot}"

class SlotAvailability(models.Model):
    date = models.DateField()
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    seats_available = models.PositiveIntegerField(default=68)
    is_blocked_for_hire = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'timeslot')

    def __str__(self):
        return f"{self.date} — {self.timeslot.timeslot} : {self.seats_available} seats"

class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
