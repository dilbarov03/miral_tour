from rest_framework import serializers

from apps.common.models import Slide, Statistics, News, Contact, MessageRequest


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ("id", "title", "text", "image")


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ("id", "title", "value", "icon")


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("id", "title", "text", "image", "published_at")


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id", "latitude", "longitude", "address", "primary_phone", "marketing_phone", "email", "instagram",
            "youtube", "facebook", "telegram"
        )


class MessageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRequest
        fields = ("id", "name", "phone", "message")
