from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, StylePreference, User


@admin.register(User)
class AuraUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "username", "is_staff", "is_active")


@admin.register(StylePreference)
class StylePreferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "body_type", "city", "onboarding_completed")
