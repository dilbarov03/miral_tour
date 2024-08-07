from modeltranslation.translator import translator, TranslationOptions

from apps.common.models import Slide, Statistics, News, Contact, NewsTag, AboutUs, DynamicPage


class SlideTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


class StatisticsTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')


class NewsTagTranslationOptions(TranslationOptions):
    fields = ('name',)


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


class ContactTranslationOptions(TranslationOptions):
    fields = ('address', 'director', 'work_time')


class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


class DynamicPageTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


translator.register(Slide, SlideTranslationOptions)
translator.register(Statistics, StatisticsTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(Contact, ContactTranslationOptions)
translator.register(NewsTag, NewsTagTranslationOptions)
translator.register(AboutUs, AboutTranslationOptions)
translator.register(DynamicPage, DynamicPageTranslationOptions)
