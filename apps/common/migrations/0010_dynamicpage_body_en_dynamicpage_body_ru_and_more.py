# Generated by Django 4.0.6 on 2024-07-14 10:00

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_dynamicpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicpage',
            name='body_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='dynamicpage',
            name='body_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='dynamicpage',
            name='body_uz',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='dynamicpage',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='dynamicpage',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='dynamicpage',
            name='title_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='Заголовок'),
        ),
    ]
