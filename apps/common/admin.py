from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.common.models import Slide, Statistics, News, Contact, MessageRequest, File, NewsTag


@admin.register(Slide)
class SlideAdmin(TranslationAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Statistics)
class StatisticsAdmin(TranslationAdmin):
    list_display = ('title', 'value', 'order')
    list_editable = ('order',)


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'published_at')
    search_fields = ('title', 'text')
    list_filter = ('published_at',)


@admin.register(Contact)
class ContactAdmin(TranslationAdmin):
    list_display = ('address', 'primary_phone', 'email')

    def has_add_permission(self, request):
        if Contact.objects.count() >= 1:
            return False
        return True


@admin.register(MessageRequest)
class MessageRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'message')
    search_fields = ('name', 'phone', 'message')
    list_filter = ('created_at',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'created_at')
    list_filter = ('created_at',)


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
