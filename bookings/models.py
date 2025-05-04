from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.

class Table(models.Model):
    table_type = models.CharField(max_length=20, choices=[
        ('table_4', 'Table for up to 4'),
        ('table_8', 'Table for up to 8'),
        ('private_room', 'Private Hire Room (10 people)')
    ], unique=True)


    name = models.CharField(max_length=100, default="Unnamed Table")
    amount_of_time_hours = models.IntegerField(default=1)

    
    def __str__(self):
        return f"{self.name} ({self.get_table_type_display()}, amount_of_time: {self.amount_of_time_hours})"


class TimeSlot(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  # Link each time slot to a table

    time = models.TimeField(unique=True, blank=False, null=False)  # Stores times like "12:00", "12:30", etc. up to 21:00
    date = models.DateField(blank=False, null=False)

    class Meta:
        ordering = ['time'] # Orders times from earliest to latest

    def __str__(self):
        return self.time.strftime("%I:%M %p")  # Formats as "12:00 PM"

class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('table', 'timeslot')  # Ensures no duplicate bookings

    def clean(self):
        """ Prevent double booking of the same table for the same time slot. """
        if Booking.objects.filter(table=self.table, timeslot=self.timeslot).exists():
            raise ValidationError("This table is already booked for the selected time.")

    def save(self, *args, **kwargs):
        """ Run validation before saving. """
        self.clean()  # Ensures validation runs before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table.name} booked at {self.time} on {self.date}"



