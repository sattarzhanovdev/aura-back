from django.contrib import admin

from .models import WeatherCache


@admin.register(WeatherCache)
class WeatherCacheAdmin(admin.ModelAdmin):
    list_display = ("city", "temp_c", "condition_main", "fetched_at")
    list_filter = ("condition_main",)
