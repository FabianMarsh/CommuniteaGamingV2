# Generated by Django 3.0.1 on 2025-05-30 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_remove_timeslot_end_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='start_time',
            new_name='timeslot',
        ),
    ]
