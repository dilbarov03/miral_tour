from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.users.models import User, SavedTour, OrderPerson, Order


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


class OrderPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPerson
        fields = ("full_name", "phone", "email", "passport_info", "passport_file", "visa", "order_call")


class OrderCreateSerializer(serializers.ModelSerializer):
    persons = OrderPersonSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tour", "tarif", "order_file", "persons")
        read_only_fields = ("id", "order_file")

    def validate(self, attrs):
        tour = attrs["tour"]
        persons = attrs["persons"]
        if len(persons) < 1:
            raise serializers.ValidationError({"persons": _("Необходимо добавить хотя бы одного участника")})
        if len(persons) > tour.people_count:
            raise serializers.ValidationError({"persons": _("Превышено максимальное количество участников")})
        return attrs

    def create(self, validated_data):
        persons = validated_data.pop("persons")
        tarif = validated_data["tarif"]
        tour = validated_data["tour"]
        order = Order.objects.create(user=self.context["request"].user, total_price=tarif.final_price,
                                     status=Order.OrderStatus.MODERATION,
                                     **validated_data)
        for person in persons:
            OrderPerson.objects.create(order=order, **person)
        tour.people_count -= len(persons)
        tour.save()
        return order
