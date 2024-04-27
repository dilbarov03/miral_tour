from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from apps.common.models import Slide, Statistics, News, Contact, MessageRequest, File
from apps.common.serializers import SlideSerializer, StatisticsSerializer, NewsSerializer, ContactSerializer, \
    MessageRequestSerializer, FileSerializer


class SlideListAPIView(generics.ListAPIView):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer


class StatisticsListAPIView(generics.ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tag',)


class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ContactAPIView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_object(self):
        return self.queryset.first()


class MessageRequestAPIView(generics.CreateAPIView):
    queryset = MessageRequest.objects.all()
    serializer_class = MessageRequestSerializer


class FileUploadAPIView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser]

