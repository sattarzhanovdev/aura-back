from urllib.parse import urljoin

import requests
from django.conf import settings


class KieAiError(Exception):
    pass


class KieAiClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {settings.KIE_API_KEY}",
                "Content-Type": "application/json",
            }
        )

    def create_task(self, *, prompt: str, image_urls: list[str], callback_url: str) -> str:
        try:
            resp = self.session.post(
                f"{settings.KIE_API_BASE}/jobs/createTask",
                json={
                    "model": "nano-banana-2",
                    "callBackUrl": callback_url,
                    "input": {
                        "prompt": prompt,
                        "image_input": image_urls,
                        "aspect_ratio": "auto",
                        "resolution": "1K",
                        "output_format": "png",
                    },
                },
                timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise KieAiError(str(exc)) from exc

        data = resp.json()
        task_id = data.get("data", {}).get("taskId")
        if not task_id:
            raise KieAiError(f"Unexpected createTask response: {data}")
        return task_id

    def get_task_detail(self, task_id: str) -> dict:
        try:
            resp = self.session.get(
                f"{settings.KIE_API_BASE}/jobs/recordInfo", params={"taskId": task_id}, timeout=15
            )
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise KieAiError(str(exc)) from exc
        return resp.json().get("data", {})


def absolute_media_url(image_field) -> str:
    """Build a URL Kie.ai (an external service) can fetch.

    Deliberately uses settings.PUBLIC_BASE_URL rather than a request's
    build_absolute_uri so this works the same way regardless of whether a
    request object is available when the job is created.
    """
    return urljoin(settings.PUBLIC_BASE_URL, image_field.url)


def build_tryon_prompt(profile, outfit_items) -> str:
    item_descriptions = ", ".join(
        f"{(item.color or '').strip()} {item.category.name.lower()} ({item.name or 'item'})".strip()
        for item in outfit_items
    )
    style_tags = ", ".join(sp.name for sp in profile.style_preferences.all()) or "casual"
    body_type = profile.get_body_type_display() if profile.body_type else "average"
    return (
        "Realistic full-body photo of the person in the reference image wearing "
        f"the following clothing items exactly as shown in the provided product photos: "
        f"{item_descriptions}. Body type: {body_type}. Style: {style_tags}. "
        "Natural lighting, neutral background, photorealistic, preserve the "
        "person's face and body identity from the reference photo."
    )
