from django.urls import path
from . import views

urlpatterns = [
    path("auth/send-code/", views.SendCodeAPIView.as_view()),
    path("auth/verify-code/", views.VerifyCodeAPIView.as_view()),
]
