from modeltranslation import translator
from modeltranslation.translator import TranslationOptions

from .models import Tour, Region, TourCategory, TourType, TourDays, Feature, TourTarif, TarifFeature


@translator.register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


@translator.register(TourCategory)
class TourCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@translator.register(TourType)
class TourTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@translator.register(Tour)
class TourTranslationOptions(TranslationOptions):
    fields = ("title", "description", "discount_text")


@translator.register(TourDays)
class TourDaysTranslationOptions(TranslationOptions):
    fields = ("title", "text", "subtitle")


@translator.register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ("title", "text")


@translator.register(TourTarif)
class TourTarifTranslationOptions(TranslationOptions):
    fields = ("title",)


@translator.register(TarifFeature)
class TarifFeatureTranslationOptions(TranslationOptions):
    fields = ("value",)
