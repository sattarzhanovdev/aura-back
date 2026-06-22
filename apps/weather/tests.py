from unittest.mock import patch

import pytest

from .models import WeatherCache
from .services import get_current_weather

OPENWEATHER_RAIN_RESPONSE = {
    "name": "Almaty",
    "main": {"temp": 8.5, "feels_like": 6.0},
    "weather": [{"main": "Rain", "description": "light rain"}],
    "wind": {"speed": 4.2},
}


@pytest.mark.django_db
@patch("apps.weather.services._fetch_from_openweather")
def test_get_current_weather_fetches_and_caches(mock_fetch):
    mock_fetch.return_value = OPENWEATHER_RAIN_RESPONSE

    weather = get_current_weather(city="Almaty")

    assert weather.temp_c == 8.5
    assert weather.condition_main == "Rain"
    assert weather.is_rainy is True
    assert weather.is_snowy is False
    assert WeatherCache.objects.count() == 1


@pytest.mark.django_db
@patch("apps.weather.services._fetch_from_openweather")
def test_get_current_weather_reuses_recent_cache(mock_fetch):
    mock_fetch.return_value = OPENWEATHER_RAIN_RESPONSE

    get_current_weather(city="Almaty")
    get_current_weather(city="Almaty")

    assert mock_fetch.call_count == 1
    assert WeatherCache.objects.count() == 1
