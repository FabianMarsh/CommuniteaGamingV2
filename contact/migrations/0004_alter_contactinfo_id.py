# Generated by Django 4.2.21 on 2025-06-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20250521_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
