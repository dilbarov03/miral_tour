from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min, Case, When, Q
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from apps.tour.models import TourType, TourCategory, Tour
from apps.tour import serializers


class TourTypeListView(generics.ListAPIView):
    queryset = TourType.objects.all()
    serializer_class = serializers.TourTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("name"),


class TourCategoryListView(generics.ListAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = serializers.TourCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("name"),


class TourDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.TourDetailSerializer

    def get_object(self):
        try:
            tour = Tour.objects.annotate(
                min_price=Min(
                    Case(
                        When(Q(tarifs__discount_price__isnull=False) & Q(discount=True),
                             then="tarifs__discount_price"),
                        default="tarifs__price",
                    )
                ),
            ).prefetch_related("images", "days", "tarifs").get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            raise Http404
        return tour
