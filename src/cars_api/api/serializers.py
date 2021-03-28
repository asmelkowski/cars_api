from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Car, Rate
from api.validators import vpic_validator


class CarSerializer(serializers.ModelSerializer):

    make = serializers.CharField()
    model = serializers.CharField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"
        validators = [
            vpic_validator,
            UniqueTogetherValidator(
                queryset=Car.objects.all(), fields=["make", "model"]
            ),
        ]

    def get_avg_rating(self, obj):
        all_ratings = obj.rate_set.all()
        if all_ratings:
            return round(sum([obj.rating for obj in all_ratings]) / len(all_ratings), 2)
        return 0


class RateSerializer(serializers.ModelSerializer):

    car_id = serializers.IntegerField()
    rating = serializers.IntegerField()
    car = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = "__all__"

    def get_car(self, obj):
        return obj.car_id

    def validate_rating(self, value):
        if value <= 0 or value > 5:
            raise serializers.ValidationError("Rating must be in range 1 - 5")
        return value


class PopularSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    make = serializers.CharField()
    model = serializers.CharField()
    rates_number = serializers.IntegerField()
