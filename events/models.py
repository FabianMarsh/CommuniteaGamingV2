from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurrence = models.CharField(
        max_length=20, choices=[
            ("none", "None"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly")
        ], default="none"
    )

    def __str__(self):
        return self.title
