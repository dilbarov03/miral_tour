# Generated by Django 4.0.6 on 2025-03-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0011_remove_tour_from_date_remove_tour_from_region_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='transfer',
        ),
        migrations.AddField(
            model_name='tour',
            name='days_count',
            field=models.IntegerField(null=True, verbose_name='Количество дней'),
        ),
    ]
