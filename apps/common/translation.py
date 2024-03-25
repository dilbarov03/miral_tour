from modeltranslation.translator import translator, TranslationOptions

from apps.common.models import Slide, Statistics, News, Contact


class SlideTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


class StatisticsTranslationOptions(TranslationOptions):
    fields = ('title',)


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


class ContactTranslationOptions(TranslationOptions):
    fields = ('address',)


translator.register(Slide, SlideTranslationOptions)
translator.register(Statistics, StatisticsTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(Contact, ContactTranslationOptions)
