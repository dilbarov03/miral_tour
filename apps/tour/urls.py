from django.urls import path

from apps.tour import views

urlpatterns = [
    path("tour-types/", views.TourTypeListView.as_view()),
    path("tour-categories/", views.TourCategoryListView.as_view()),
    path("tour/<int:pk>/", views.TourDetailView.as_view()),
]
