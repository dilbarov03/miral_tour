from rest_framework import serializers

from apps.common.models import Slide, Statistics, News, Contact, MessageRequest, File, NewsTag, AboutUs, DynamicPage


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ("id", "title", "text", "image")


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ("id", "title", "subtitle", "value", "icon")


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ("id", "name")


class NewsSerializer(serializers.ModelSerializer):
    tag = NewsTagSerializer(read_only=True)

    class Meta:
        model = News
        fields = ("id", "title", "tag", "text", "image", "published_at")


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id", "latitude", "longitude", "address", "primary_phone", "marketing_phone", "email", "instagram",
            "youtube", "facebook", "telegram", "whatsapp"
        )


class MessageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRequest
        fields = ("id", "name", "phone", "message")


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "file")


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ("id", "title", "body")


class DynamicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicPage
        fields = ("id", "title", "body")
