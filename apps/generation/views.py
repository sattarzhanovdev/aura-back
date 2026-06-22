import secrets
from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.outfits.models import Outfit

from .models import GenerationJob
from .result_handling import apply_kie_result
from .serializers import GenerationJobSerializer
from .services import KieAiClient, KieAiError, absolute_media_url, build_tryon_prompt

BACKSTOP_POLL_AFTER = timedelta(seconds=20)


class CreateGenerationJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        outfit_id = request.data.get("outfit_id")
        if not outfit_id:
            return Response({"detail": "outfit_id is required."}, status=400)

        outfit = get_object_or_404(Outfit, pk=outfit_id, user=request.user)
        outfit_items = [oi.clothing_item for oi in outfit.items.select_related("clothing_item__category")]
        if not outfit_items:
            return Response({"detail": "This outfit has no items."}, status=422)

        profile = request.user.profile
        if not profile.reference_photo:
            return Response({"detail": "Add a reference photo in onboarding first."}, status=422)

        prompt = build_tryon_prompt(profile, outfit_items)
        image_urls = [absolute_media_url(profile.reference_photo)] + [
            absolute_media_url(item.photo) for item in outfit_items
        ]

        job = GenerationJob.objects.create(
            user=request.user,
            outfit=outfit,
            prompt=prompt,
            input_image_urls=image_urls,
            callback_token=secrets.token_urlsafe(32),
        )

        callback_url = urljoin(settings.PUBLIC_BASE_URL, f"/api/callback/{job.callback_token}/")
        try:
            task_id = KieAiClient().create_task(
                prompt=prompt, image_urls=image_urls, callback_url=callback_url
            )
        except KieAiError as exc:
            job.status = "failed"
            job.error_message = str(exc)
            job.save()
            return Response(GenerationJobSerializer(job, context={"request": request}).data, status=502)

        job.kie_task_id = task_id
        job.status = "processing"
        job.save()
        return Response(GenerationJobSerializer(job, context={"request": request}).data, status=201)


class GenerationJobDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GenerationJobSerializer

    def get_queryset(self):
        return GenerationJob.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        job = self.get_object()
        if (
            job.status in ("pending", "processing")
            and job.kie_task_id
            and timezone.now() - job.updated_at > BACKSTOP_POLL_AFTER
        ):
            try:
                detail = KieAiClient().get_task_detail(job.kie_task_id)
                apply_kie_result(job, {"data": detail})
                job.refresh_from_db()
            except KieAiError:
                pass  # webhook may still arrive; don't fail the poll request
        return Response(GenerationJobSerializer(job, context={"request": request}).data)
