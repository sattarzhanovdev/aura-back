from rest_framework import serializers

from apps.wardrobe.serializers import ClothingItemSerializer
from apps.weather.serializers import WeatherCacheSerializer

from .models import Outfit, OutfitItem


class OutfitItemSerializer(serializers.ModelSerializer):
    clothing_item = ClothingItemSerializer(read_only=True)

    class Meta:
        model = OutfitItem
        fields = ["id", "clothing_item"]


class OutfitSerializer(serializers.ModelSerializer):
    items = OutfitItemSerializer(many=True, read_only=True)
    weather_snapshot = WeatherCacheSerializer(read_only=True)

    class Meta:
        model = Outfit
        fields = ["id", "status", "weather_snapshot", "items", "created_at"]
        read_only_fields = ["id", "weather_snapshot", "items", "created_at"]


class OutfitStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ["status"]
