from modeltranslation.translator import translator, TranslationOptions

from apps.common.models import Slide, Statistics, News, Contact, NewsTag


class SlideTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


class StatisticsTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')


class NewsTagTranslationOptions(TranslationOptions):
    fields = ('name',)


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


class ContactTranslationOptions(TranslationOptions):
    fields = ('address',)


translator.register(Slide, SlideTranslationOptions)
translator.register(Statistics, StatisticsTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(Contact, ContactTranslationOptions)
translator.register(NewsTag, NewsTagTranslationOptions)
