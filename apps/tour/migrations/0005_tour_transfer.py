# Generated by Django 4.0.6 on 2024-04-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0004_tour_is_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='transfer',
            field=models.BooleanField(default=False, verbose_name='Трансфер включен'),
        ),
    ]
