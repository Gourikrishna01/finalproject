# Generated by Django 5.0.1 on 2024-02-27 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0012_reservation_itinerary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='itinerary',
        ),
    ]
