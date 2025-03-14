from rest_framework import serializers

from .models import TourType, TourCategory, TourDays, TourImage, Feature, TourFeature, TarifFeature, TourTarif, Tour, \
    RegionTour


class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCategory
        fields = ("id", "name")


class TourTypeSerializer(serializers.ModelSerializer):
    categories = TourCategorySerializer(many=True)

    class Meta:
        model = TourType
        fields = ("id", "name", "image", "categories")


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ("id", "image")


class TourDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDays
        fields = ("id", "title", "subtitle", "text")


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("id", "title", "text", "file")


class TourFeatureSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer(read_only=True)

    class Meta:
        model = TourFeature
        fields = ("id", "feature", "included", "value")


class TarifFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifFeature
        fields = ("id", "included", "value")


class TourTarifSerializer(serializers.ModelSerializer):
    features = TarifFeatureSerializer(many=True)

    class Meta:
        model = TourTarif
        fields = ("id", "title", "price", "discount_price", "features")


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class TourListSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ("id", "title", "slug", "description", "main_image", "period", "days_count", "discount",
                  "discount_text", "min_price", "origin_start_price", "is_saved")

    def get_is_saved(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.saved_tours.filter(user=user).exists()
        return False


class RegionTourSerializer(serializers.ModelSerializer):
    tour = TourListSerializer()
    region = RegionSerializer()

    class Meta:
        model = RegionTour
        fields = ("id", "region", "tour", "image")


class TourDetailSerializer(serializers.ModelSerializer):
    region_one = RegionSerializer()
    region_two = RegionSerializer()
    region_three = RegionSerializer()
    region_four = RegionSerializer()
    region_five = RegionSerializer()
    images = TourImageSerializer(many=True)
    days = TourDaysSerializer(many=True)
    features = TourFeatureSerializer(many=True)
    tarifs = TourTarifSerializer(many=True)
    min_price = serializers.IntegerField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ("id", "title", "slug", "description", "main_image",
                  "region_one", "region_two", "region_three", "region_four", "region_five",
                  "period", "days_count", "video_link", "video", "people_count", "discount", "discount_text",
                  "images", "days", "features", "tarifs", "min_price", "is_saved")

    def get_is_saved(self, obj):
        if self.context.get("request").user.is_authenticated:
            return obj.saved_tours.filter(user=self.context.get("request").user).exists()
        return False
