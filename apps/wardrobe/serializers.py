from rest_framework import serializers

from .models import Category, ClothingItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "warmth_relevant"]


class ClothingItemSerializer(serializers.ModelSerializer):
    category_slug = serializers.SlugRelatedField(
        source="category", slug_field="slug", queryset=Category.objects.all(), write_only=True
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ClothingItem
        fields = [
            "id",
            "category",
            "category_slug",
            "photo",
            "name",
            "color",
            "warmth_level",
            "is_waterproof",
            "season",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "is_active", "created_at"]
