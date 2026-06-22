from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from .models import WeatherCache

CACHE_TTL_MINUTES = 20
RAINY_CONDITIONS = {"Rain", "Thunderstorm", "Drizzle"}
SNOWY_CONDITIONS = {"Snow"}


class WeatherFetchError(Exception):
    pass


def _build_cache_entry(city: str, lat, lon, data: dict) -> WeatherCache:
    main = data["weather"][0]["main"]
    return WeatherCache.objects.create(
        city=city,
        lat=lat,
        lon=lon,
        temp_c=data["main"]["temp"],
        feels_like_c=data["main"]["feels_like"],
        condition_main=main,
        condition_description=data["weather"][0]["description"],
        is_rainy=main in RAINY_CONDITIONS,
        is_snowy=main in SNOWY_CONDITIONS,
        wind_speed=data.get("wind", {}).get("speed", 0),
        raw_response=data,
    )


def _fetch_from_openweather(params: dict) -> dict:
    params = {**params, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"}
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise WeatherFetchError(str(exc)) from exc
    return resp.json()


def get_current_weather(city: str | None = None, lat: float | None = None, lon: float | None = None) -> WeatherCache:
    if not city and (lat is None or lon is None):
        raise ValueError("Either city or lat/lon must be provided.")

    cache_key = city or f"{lat},{lon}"
    cutoff = timezone.now() - timedelta(minutes=CACHE_TTL_MINUTES)
    cached = WeatherCache.objects.filter(city=cache_key, fetched_at__gte=cutoff).order_by("-fetched_at").first()
    if cached:
        return cached

    params = {"q": city} if city else {"lat": lat, "lon": lon}
    data = _fetch_from_openweather(params)
    # Store under cache_key (not the API's resolved city name) so the next
    # lookup with the same input always hits this cache row.
    return _build_cache_entry(cache_key, lat, lon, data)
