# Generated by Django 4.0.6 on 2024-03-30 06:58

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_feature_text_en_feature_text_ru_feature_text_uz_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=85, scale=None, size=[1920, 1080], upload_to='region_tours', verbose_name='Изображение')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_tours', to='tour.region', unique=True, verbose_name='Регион')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_tours', to='tour.tour', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Тур региона',
                'verbose_name_plural': 'Туры регионов',
            },
        ),
    ]
