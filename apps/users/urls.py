from django.urls import path
from . import views

urlpatterns = [
    path("auth/send-code/", views.SendCodeAPIView.as_view()),
    path("auth/verify-code/", views.VerifyCodeAPIView.as_view()),
    path("profile/", views.UserProfileAPIView.as_view()),
    path("profile/delete/", views.UserDeleteAPIView.as_view()),
    path("saved-tours/", views.SavedTourAPIView.as_view()),
    path("saved-tours/change/", views.SavedTourCreateView.as_view()),
    path("orders/create/", views.OrderCreateView.as_view()),
]
