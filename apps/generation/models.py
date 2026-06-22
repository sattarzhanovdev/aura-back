from django.conf import settings
from django.db import models

from apps.outfits.models import Outfit


class GenerationJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generation_jobs")
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name="generation_jobs")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    kie_task_id = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    # Embedded in the callback URL path so Kie.ai's unauthenticated webhook
    # can be matched back to this job without trusting payload content alone.
    callback_token = models.CharField(max_length=64, unique=True, db_index=True)
    prompt = models.TextField()
    input_image_urls = models.JSONField(default=list)
    result_image = models.ImageField(upload_to="generated/%Y/%m/", null=True, blank=True)
    result_image_url_external = models.URLField(blank=True)
    error_message = models.TextField(blank=True)
    raw_callback_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"GenerationJob #{self.pk} ({self.status})"
