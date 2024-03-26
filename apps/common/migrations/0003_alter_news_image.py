# Generated by Django 4.0.6 on 2024-03-25 11:04

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_contact_address_en_contact_address_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=85, scale=None, size=[1920, 1080], upload_to='news', verbose_name='Изображение'),
        ),
    ]