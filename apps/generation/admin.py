from django.contrib import admin

from .models import GenerationJob


@admin.register(GenerationJob)
class GenerationJobAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "outfit", "status", "kie_task_id", "created_at")
    list_filter = ("status",)
    readonly_fields = ("callback_token", "raw_callback_payload")
