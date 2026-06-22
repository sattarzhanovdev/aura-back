from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import Profile, StylePreference, User


class StylePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StylePreference
        fields = ["id", "name", "slug"]


class ProfileSerializer(serializers.ModelSerializer):
    style_preferences = StylePreferenceSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "body_type",
            "height_cm",
            "weight_kg",
            "style_preferences",
            "reference_photo",
            "city",
            "onboarding_completed",
        ]
        read_only_fields = ["onboarding_completed"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    style_preferences = serializers.PrimaryKeyRelatedField(
        many=True, queryset=StylePreference.objects.all(), required=False
    )

    class Meta:
        model = Profile
        fields = ["body_type", "height_cm", "weight_kg", "style_preferences", "city"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "profile"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
