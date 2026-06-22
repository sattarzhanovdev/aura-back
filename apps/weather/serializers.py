from rest_framework import serializers

from .models import WeatherCache


class WeatherCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCache
        fields = [
            "id",
            "city",
            "lat",
            "lon",
            "temp_c",
            "feels_like_c",
            "condition_main",
            "condition_description",
            "is_rainy",
            "is_snowy",
            "wind_speed",
            "fetched_at",
        ]
