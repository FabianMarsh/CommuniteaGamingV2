# Generated by Django 3.0.1 on 2025-05-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='address_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='what_three_words_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
