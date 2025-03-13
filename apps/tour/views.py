from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.tour.filters import TourFilterSet
from apps.tour.models import TourType, TourCategory, Tour, RegionTour
from apps.tour import serializers


class TourTypeListView(generics.ListAPIView):
    queryset = TourType.objects.prefetch_related("categories")
    serializer_class = serializers.TourTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("name",),


class TourCategoryListView(generics.ListAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = serializers.TourCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("name",),
    filterset_fields = ("tour_type",)


class TourDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.TourDetailSerializer
    queryset = Tour.objects.all()

    def get_object(self):
        try:
            tour = Tour.objects.prefetch_related("images", "days", "tarifs").get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            raise Http404
        return tour


class RegionTourListView(generics.ListAPIView):
    serializer_class = serializers.RegionTourSerializer
    queryset = RegionTour.objects.all()


class TourListView(generics.ListAPIView):
    serializer_class = serializers.TourListSerializer
    queryset = Tour.objects.active()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("title",)
    filterset_fields = ("category", "tour_type", "region_one", "region_two", "region_three", "period",
                        "is_popular", "discount")


class SimilarTourListView(generics.ListAPIView):
    serializer_class = serializers.TourListSerializer

    def get_queryset(self):
        tour = get_object_or_404(Tour, pk=self.kwargs["pk"])
        return Tour.objects.filter(
            category=tour.category,
            tour_type__in=tour.tour_type.all(),
        ).exclude(pk=tour.pk).order_by("?")[:4]


class TourFilterView(generics.ListAPIView):
    serializer_class = serializers.TourListSerializer
    queryset = Tour.objects.active()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("title",)
    filterset_class = TourFilterSet
