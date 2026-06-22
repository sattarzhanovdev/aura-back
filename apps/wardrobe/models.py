from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    # Whether this category's warmth/season matters for the outfit engine
    # (e.g. accessories generally don't drive warmth decisions).
    warmth_relevant = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class ClothingItem(models.Model):
    WARMTH_CHOICES = [
        (1, "Light"),
        (2, "Medium"),
        (3, "Warm"),
        (4, "Very warm"),
    ]
    SEASON_CHOICES = [
        ("all", "All season"),
        ("summer", "Summer"),
        ("winter", "Winter"),
        ("spring_fall", "Spring/Fall"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wardrobe_items")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    photo = models.ImageField(upload_to="wardrobe/%Y/%m/")
    name = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=30, blank=True)
    warmth_level = models.PositiveSmallIntegerField(choices=WARMTH_CHOICES, default=2)
    is_waterproof = models.BooleanField(default=False)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, default="all")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or f"{self.category.name} item #{self.pk}"
