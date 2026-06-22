import json

import requests
from django.core.files.base import ContentFile

from .models import GenerationJob


def apply_kie_result(job: GenerationJob, payload: dict) -> None:
    """Shared logic between the webhook callback and the polling backstop."""
    if job.status in ("succeeded", "failed"):
        return  # idempotent: ignore retried/duplicate callbacks

    data = payload.get("data", payload)
    state = data.get("state")
    job.raw_callback_payload = payload

    if state == "success":
        result_json = data.get("resultJson")
        if isinstance(result_json, str):
            result_json = json.loads(result_json)
        url = result_json["resultUrls"][0]
        # Kie.ai-hosted result URLs expire (~24h) -- download immediately.
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        job.result_image.save(f"job_{job.id}.png", ContentFile(resp.content), save=False)
        job.result_image_url_external = url
        job.status = "succeeded"
    elif state == "fail":
        job.status = "failed"
        job.error_message = data.get("failMsg", "Generation failed.")

    job.save()
