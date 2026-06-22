from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WeatherCacheSerializer
from .services import WeatherFetchError, get_current_weather


class CurrentWeatherView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        city = request.query_params.get("city")
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        if not city and not (lat and lon):
            city = request.user.profile.city or None
        if not city and not (lat and lon):
            return Response(
                {"detail": "Provide ?city= or ?lat=&lon=, or set a city in your profile."},
                status=400,
            )

        try:
            weather = get_current_weather(
                city=city,
                lat=float(lat) if lat else None,
                lon=float(lon) if lon else None,
            )
        except WeatherFetchError:
            return Response({"detail": "Could not fetch weather right now."}, status=502)

        return Response(WeatherCacheSerializer(weather).data)
