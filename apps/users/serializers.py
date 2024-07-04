from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.tour.serializers import TourListSerializer
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
        fields = ("id", "full_name", "phone", "email", "passport_info", "passport_file", "visa", "order_call")


class OrderCreateSerializer(serializers.ModelSerializer):
    persons = OrderPersonSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tour", "tarif", "order_file", "persons", "currency")
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

        with transaction.atomic():
            order = Order.objects.create(
                user=self.context["request"].user,
                total_price=tarif.final_price * len(persons),
                status=Order.OrderStatus.MODERATION,
                **validated_data
            )
            for person in persons:
                OrderPerson.objects.create(order=order, **person)
            tour.people_count -= len(persons)
            tour.save()

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    persons = OrderPersonSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "persons", "currency")

    def validate(self, attrs):
        persons = attrs["persons"]
        tour = self.instance.tour
        if len(persons) < 1:
            raise serializers.ValidationError({"persons": _("Необходимо добавить хотя бы одного участника")})
        if tour.people_count + len(self.instance.persons.all()) < len(persons):
            raise serializers.ValidationError({"persons": _("Превышено максимальное количество участников")})
        return attrs

    def update(self, instance, validated_data):
        persons = validated_data.pop("persons")
        tour = instance.tour

        with transaction.atomic():
            # Fetch and delete the old order people
            old_order_people = OrderPerson.objects.filter(order=instance)
            old_order_people_count = old_order_people.count()
            old_order_people.delete()

            # Create new order people
            new_order_people = [OrderPerson(order=instance, **person) for person in persons]
            OrderPerson.objects.bulk_create(new_order_people)

            # Update the people count and save the tour
            tour.people_count += old_order_people_count - len(persons)
            tour.save()

            # Update the total price and save the instance
            instance.total_price = instance.tarif.final_price * len(persons)
            instance.currency = validated_data.get("currency", instance.currency)
            instance.save()

        return instance


class UserOrderSerializer(serializers.ModelSerializer):
    tour = TourListSerializer()

    class Meta:
        model = Order
        fields = ("id", "tour", "status", "total_price", "order_file", "created_at", "currency")
