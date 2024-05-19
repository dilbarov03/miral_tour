from django_filters import rest_framework as filters

from apps.tour.models import Tour


class TourFilterSet(filters.FilterSet):
    # There should be such filters:
    # - Date: date the tour starts
    # - tourist count: number of tourists. The tour should have enough free places for this number of tourists
    # - place: which place tour goes to, foreign key to Region
    # - type: type of the tour, foreign key to TourType
    # - excursion: if the tour includes excursions, boolean. It will look if TourFeature with name "excursion" exists

    date = filters.DateFilter(field_name="from_date", lookup_expr="exact", label="Дата")
    tourist_count = filters.NumberFilter(field_name="people_count", lookup_expr="gte", label="Количество туристов")
    place = filters.NumberFilter(field_name="to_region_id", lookup_expr="exact", label="Место")
    type = filters.NumberFilter(field_name="tour_type_id", lookup_expr="exact", label="Тип тура")
    excursion = filters.BooleanFilter(method="filter_excursion", label="Экскурсия")

    class Meta:
        model = Tour
        fields = ["date", "tourist_count", "place", "type", "excursion"]

    def filter_excursion(self, queryset, name, value):
        return queryset.filter(features__feature__name_ru="Экскурсия", features__included=value)
