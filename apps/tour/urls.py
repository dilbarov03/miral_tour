from django.urls import path

from apps.tour import views

urlpatterns = [
    path("tour-types/", views.TourTypeListView.as_view()),
    path("tour-categories/", views.TourCategoryListView.as_view()),
    path("region-tours/", views.RegionTourListView.as_view()),
    path("tour/", views.TourListView.as_view()),
    path("tour/filter/", views.TourFilterView.as_view()),
    path("tour/<slug:slug>/", views.TourDetailView.as_view()),
    path("tour/<slug:slug>/similar/", views.SimilarTourListView.as_view()),
]
