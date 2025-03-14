from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline
from .models import Tour, Region, TourCategory, TourType, TourDays, Feature, TourTarif, TarifFeature, TourImage, \
    TourFeature, RegionTour


@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "order")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(TourCategory)
class TourCategoryAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "tour_type", "order")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("tour_type",)


@admin.register(TourType)
class TourTypeAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "order")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(Feature)
class FeatureAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "text")
    list_display_links = ("id", "title")
    search_fields = ("title", "text")


class TourImagesInline(admin.TabularInline):
    model = TourImage
    extra = 0


class TourDaysInline(TranslationStackedInline):
    model = TourDays
    extra = 0


class TourFeatureInline(admin.TabularInline):
    model = TourFeature
    extra = 0


class TourTarifInline(TranslationStackedInline):
    model = TourTarif
    extra = 0


@admin.register(Tour)
class TourAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "category", )
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_filter = ("category", "tour_type", "region_one", "region_two", "region_three",
                   "period", "is_active", "discount", "is_popular")
    inlines = (TourImagesInline, TourDaysInline, TourFeatureInline, TourTarifInline)
    autocomplete_fields = ("region_one", "region_two", "region_three", "region_four", "region_five",
                           "category")


class TarifFeatureInline(TranslationTabularInline):
    model = TarifFeature


@admin.register(TourTarif)
class TourTarifAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "tour")
    list_display_links = ("id", "title")
    search_fields = ("title", "tour__title")
    list_filter = ("tour",)
    inlines = (TarifFeatureInline,)


@admin.register(RegionTour)
class RegionTourAdmin(admin.ModelAdmin):
    list_display = ("id", "region", "tour")
    list_display_links = ("id", "region")
    search_fields = ("region__name", "tour__title")
    list_filter = ("region", "tour")
