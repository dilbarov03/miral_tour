from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.users.models import User, SavedTour


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email", "phone")


class SavedTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedTour
        fields = ("tour",)

    def create(self, validated_data):
        saved_tour = SavedTour.objects.filter(user=self.context["request"].user, tour=validated_data["tour"]).first()
        if saved_tour:
            saved_tour.delete()
            action = "delete"
        else:
            saved_tour = SavedTour.objects.create(user=self.context["request"].user, **validated_data)
            action = "create"
        self.context["action"] = action
        return saved_tour

    def to_representation(self, instance):
        if self.context["action"] == "create":
            return {"msg": _("Тур успешно сохранен")}
        return {"msg": _("Тур успешно удален")}
