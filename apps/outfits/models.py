from django.conf import settings
from django.db import models

from apps.wardrobe.models import ClothingItem
from apps.weather.models import WeatherCache


class Outfit(models.Model):
    STATUS_CHOICES = [
        ("suggested", "Suggested"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outfits")
    weather_snapshot = models.ForeignKey(
        WeatherCache, null=True, blank=True, on_delete=models.SET_NULL, related_name="outfits"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="suggested")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Outfit #{self.pk} for {self.user.email}"


class OutfitItem(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name="items")
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("outfit", "clothing_item")
