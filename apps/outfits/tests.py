import pytest

from apps.accounts.models import User
from apps.wardrobe.models import Category, ClothingItem
from apps.weather.models import WeatherCache

from .exceptions import InsufficientWardrobeError
from .services import suggest_outfit


@pytest.fixture
def user(db):
    return User.objects.create_user(username="jane", email="jane@example.com", password="x")


@pytest.fixture
def categories(db):
    return {
        slug: Category.objects.create(name=slug.title(), slug=slug)
        for slug in ["tops", "bottoms", "shoes", "outerwear"]
    }


def make_item(user, category, **kwargs):
    defaults = {"photo": "wardrobe/test.png", "warmth_level": 2, "is_waterproof": False}
    defaults.update(kwargs)
    return ClothingItem.objects.create(user=user, category=category, **defaults)


def make_weather(temp_c, is_rainy=False, **kwargs):
    defaults = {
        "city": "TestCity",
        "feels_like_c": temp_c,
        "condition_main": "Rain" if is_rainy else "Clear",
        "condition_description": "test",
        "is_rainy": is_rainy,
        "raw_response": {},
    }
    defaults.update(kwargs)
    return WeatherCache.objects.create(temp_c=temp_c, **defaults)


@pytest.mark.django_db
def test_cold_rainy_weather_prefers_outerwear_and_waterproof_shoes(user, categories):
    make_item(user, categories["tops"], name="warm top", warmth_level=4)
    make_item(user, categories["bottoms"], name="warm pants", warmth_level=4)
    make_item(user, categories["shoes"], name="dry shoes", warmth_level=2, is_waterproof=False)
    waterproof_shoes = make_item(
        user, categories["shoes"], name="rain boots", warmth_level=2, is_waterproof=True
    )
    make_item(user, categories["outerwear"], name="coat", warmth_level=4)

    weather = make_weather(temp_c=1, is_rainy=True)
    outfit = suggest_outfit(user, weather)

    items_by_category = {i.clothing_item.category.slug: i.clothing_item for i in outfit.items.all()}
    assert "outerwear" in items_by_category
    assert items_by_category["shoes"] == waterproof_shoes


@pytest.mark.django_db
def test_warm_weather_skips_outerwear(user, categories):
    make_item(user, categories["tops"], name="t-shirt", warmth_level=1)
    make_item(user, categories["bottoms"], name="shorts", warmth_level=1)
    make_item(user, categories["shoes"], name="sandals", warmth_level=1)
    make_item(user, categories["outerwear"], name="coat", warmth_level=4)

    weather = make_weather(temp_c=28, is_rainy=False)
    outfit = suggest_outfit(user, weather)

    categories_used = {i.clothing_item.category.slug for i in outfit.items.all()}
    assert "outerwear" not in categories_used
    assert {"tops", "bottoms", "shoes"} <= categories_used


@pytest.mark.django_db
def test_sparse_wardrobe_raises_insufficient_wardrobe_error(user, categories):
    make_item(user, categories["tops"], name="t-shirt", warmth_level=2)
    # No bottoms or shoes added.

    weather = make_weather(temp_c=20, is_rainy=False)

    with pytest.raises(InsufficientWardrobeError) as exc_info:
        suggest_outfit(user, weather)

    assert set(exc_info.value.missing_categories) == {"bottoms", "shoes"}
