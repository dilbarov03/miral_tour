# Generated by Django 4.0.6 on 2024-07-14 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='refund_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
