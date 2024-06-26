# Generated by Django 4.0.6 on 2024-03-26 10:18

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('file', models.FileField(blank=True, null=True, upload_to='features', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('main_image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=85, scale=None, size=[1920, 1080], upload_to='tours', verbose_name='Главное изображение')),
                ('from_date', models.DateField(verbose_name='Дата начала')),
                ('to_date', models.DateField(verbose_name='Дата окончания')),
                ('video_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')),
                ('video', models.FileField(blank=True, null=True, upload_to='tour_videos', verbose_name='Видео')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('people_count', models.IntegerField(verbose_name='Количество людей')),
                ('discount', models.BooleanField(default=False, verbose_name='Скидка')),
                ('discount_text', models.TextField(blank=True, null=True, verbose_name='Текст скидки')),
            ],
            options={
                'verbose_name': 'Тур',
                'verbose_name_plural': 'Туры',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TourCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Категория тура',
                'verbose_name_plural': 'Категории туров',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TourType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=85, scale=None, size=[1920, 1080], upload_to='tour_types', verbose_name='Изображение')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Тип тура',
                'verbose_name_plural': 'Типы туров',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TourTarif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена со скидкой')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifs', to='tour.tour', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=85, scale=None, size=[1920, 1080], upload_to='tour_images', verbose_name='Изображение')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tour.tour', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Изображение тура',
                'verbose_name_plural': 'Изображения туров',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TourFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('included', models.BooleanField(default=True, verbose_name='Включено')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Значение')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tour.feature', verbose_name='Услуга')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='tour.tour', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Услуга тура',
                'verbose_name_plural': 'Услуги туров',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TourDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='tour.tour', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'День тура',
                'verbose_name_plural': 'Дни туров',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='tour',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tour.tourcategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='tour',
            name='from_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tour.region', verbose_name='Откуда'),
        ),
        migrations.AddField(
            model_name='tour',
            name='return_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours_return', to='tour.region', verbose_name='Обратно'),
        ),
        migrations.AddField(
            model_name='tour',
            name='to_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours_to', to='tour.region', verbose_name='Куда'),
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='tour.tourtype', verbose_name='Тип тура'),
        ),
        migrations.CreateModel(
            name='TarifFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('included', models.BooleanField(default=True, verbose_name='Включено')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Значение')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок')),
                ('tarif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='tour.tourtarif', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'Услуга тарифа',
                'verbose_name_plural': 'Услуги тарифов',
                'ordering': ['order'],
            },
        ),
    ]
