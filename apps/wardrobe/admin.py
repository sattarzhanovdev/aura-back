from django.contrib import admin

from .models import Category, ClothingItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "warmth_relevant")


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "warmth_level", "season", "is_active")
    list_filter = ("category", "season", "is_active")
