# Generated by Django 4.0.6 on 2024-03-30 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_regiontour'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='Популярный'),
        ),
    ]
