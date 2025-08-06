from django import forms
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from .models import Event

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

    list_display = ("title", "date", "start_time", "end_time")
    search_fields = ("title", "description") 
    ordering = ("date", "start_time") 

    # override save func with view recurrence logic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        recurrence = obj.recurrence
        event_date = obj.date

        if not change and recurrence in ["daily", "weekly", "monthly"]:
            for i in range(1, 5):
                if recurrence == "daily":
                    new_date = event_date + timedelta(days=i)
                elif recurrence == "weekly":
                    new_date = event_date + timedelta(weeks=i)
                elif recurrence == "monthly":
                    try:
                        new_date = event_date + relativedelta(months=i)
                    except ValueError:
                        new_date = event_date.replace(day=28) + relativedelta(months=i)

                Event.objects.create(
                    title=obj.title,
                    description=obj.description,
                    date=new_date,
                    start_time=obj.start_time,
                    end_time=obj.end_time,
                    recurrence=recurrence
                )


