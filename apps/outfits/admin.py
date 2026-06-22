from django.contrib import admin

from .models import Outfit, OutfitItem


class OutfitItemInline(admin.TabularInline):
    model = OutfitItem
    extra = 0


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at")
    inlines = [OutfitItemInline]
