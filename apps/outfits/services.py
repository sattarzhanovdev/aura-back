import random

from apps.wardrobe.models import ClothingItem
from apps.weather.models import WeatherCache

from .constants import (
    OPTIONAL_CATEGORY_SLUGS,
    OUTERWEAR_MIN_WARMTH,
    REQUIRED_CATEGORY_SLUGS,
    WARMTH_TEMP_THRESHOLDS,
    DEFAULT_WARMTH_LEVEL,
)
from .exceptions import InsufficientWardrobeError
from .models import Outfit, OutfitItem


def warmth_for_temp(temp_c: float) -> int:
    for threshold, level in WARMTH_TEMP_THRESHOLDS:
        if temp_c < threshold:
            return level
    return DEFAULT_WARMTH_LEVEL


def _filter_by_warmth(items, target_warmth: int):
    """Prefer items within +/-1 of the target warmth; widen the search if empty."""
    close = [i for i in items if abs(i.warmth_level - target_warmth) <= 1]
    return close or list(items)


def _filter_by_waterproof(items, is_rainy: bool):
    """When it's rainy, restrict to waterproof items if any are available."""
    if not is_rainy:
        return items
    waterproof = [i for i in items if i.is_waterproof]
    return waterproof or items


def _pick_best(items, style_preference_ids: set[int]):
    if not items:
        return None
    if style_preference_ids:
        # Tie-break only: prefer items whose user has matching style tags is
        # not modeled on ClothingItem yet, so for now this is a no-op hook
        # for a future style-tag field. Random choice keeps variety.
        pass
    return random.choice(list(items))


def _select_for_category(pool, slug: str, target_warmth: int, is_rainy: bool, style_preference_ids: set[int]):
    candidates = [item for item in pool if item.category.slug == slug]
    candidates = _filter_by_warmth(candidates, target_warmth)
    candidates = _filter_by_waterproof(candidates, is_rainy)
    return _pick_best(candidates, style_preference_ids)


def suggest_outfit(user, weather: WeatherCache) -> Outfit:
    target_warmth = warmth_for_temp(weather.temp_c)
    pool = list(
        ClothingItem.objects.filter(user=user, is_active=True).select_related("category")
    )

    style_preference_ids = set(
        user.profile.style_preferences.values_list("id", flat=True)
    )

    chosen: dict[str, ClothingItem] = {}
    missing: list[str] = []

    for slug in REQUIRED_CATEGORY_SLUGS:
        item = _select_for_category(pool, slug, target_warmth, weather.is_rainy, style_preference_ids)
        if item:
            chosen[slug] = item
        else:
            missing.append(slug)

    if missing:
        raise InsufficientWardrobeError(missing)

    if target_warmth >= OUTERWEAR_MIN_WARMTH:
        for slug in OPTIONAL_CATEGORY_SLUGS:
            item = _select_for_category(pool, slug, target_warmth, weather.is_rainy, style_preference_ids)
            if item:
                chosen[slug] = item

    outfit = Outfit.objects.create(user=user, weather_snapshot=weather)
    OutfitItem.objects.bulk_create(
        [OutfitItem(outfit=outfit, clothing_item=item) for item in chosen.values()]
    )
    return outfit
