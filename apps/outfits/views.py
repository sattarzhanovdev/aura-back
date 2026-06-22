from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.weather.services import WeatherFetchError, get_current_weather

from .exceptions import InsufficientWardrobeError
from .models import Outfit
from .serializers import OutfitSerializer, OutfitStatusUpdateSerializer
from .services import suggest_outfit


class SuggestOutfitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        city = request.data.get("city") or request.user.profile.city or None
        lat = request.data.get("lat")
        lon = request.data.get("lon")

        if not city and not (lat and lon):
            return Response(
                {"detail": "Provide city or lat/lon, or set a city in your profile."},
                status=400,
            )

        try:
            weather = get_current_weather(
                city=city, lat=float(lat) if lat else None, lon=float(lon) if lon else None
            )
        except WeatherFetchError:
            return Response({"detail": "Could not fetch weather right now."}, status=502)

        try:
            outfit = suggest_outfit(request.user, weather)
        except InsufficientWardrobeError as exc:
            return Response(
                {"detail": str(exc), "missing_categories": exc.missing_categories},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(OutfitSerializer(outfit, context={"request": request}).data, status=201)


class OutfitDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OutfitStatusUpdateSerializer
        return OutfitSerializer

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(OutfitSerializer(self.get_object(), context={"request": request}).data)
