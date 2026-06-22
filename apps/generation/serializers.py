from rest_framework import serializers

from .models import GenerationJob


class GenerationJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationJob
        fields = [
            "id",
            "outfit",
            "status",
            "result_image",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
