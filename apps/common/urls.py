from django.urls import path

from apps.common.views import SlideListAPIView, StatisticsListAPIView, NewsListAPIView, NewsDetailAPIView, \
    ContactAPIView, MessageRequestAPIView, FileUploadAPIView, AboutUsAPIView, DynamicPageAPIView

urlpatterns = [
    path("slides/", SlideListAPIView.as_view(), name="slide-list"),
    path("statistics/", StatisticsListAPIView.as_view(), name="statistics-list"),
    path("news/", NewsListAPIView.as_view(), name="news-list"),
    path("news/<int:pk>/", NewsDetailAPIView.as_view(), name="news-detail"),
    path("contacts/", ContactAPIView.as_view(), name="contact-detail"),
    path("message-request/", MessageRequestAPIView.as_view(), name="message-request"),
    path("file-upload/", FileUploadAPIView.as_view(), name="file-upload"),
    path("about-us/", AboutUsAPIView.as_view(), name="about-us"),
    path("dynamic-page/<slug:slug>/", DynamicPageAPIView.as_view(), name="dynamic-page"),
]
