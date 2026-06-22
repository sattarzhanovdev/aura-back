from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GenerationJob
from .result_handling import apply_kie_result


class KieCallbackView(APIView):
    # DRF's APIView.as_view() already wraps the view in django's csrf_exempt,
    # which is required here since Kie.ai's webhook calls in with no CSRF token.
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, callback_token):
        job = get_object_or_404(GenerationJob, callback_token=callback_token)
        payload = request.data

        task_id = payload.get("data", {}).get("taskId")
        if job.kie_task_id and task_id and task_id != job.kie_task_id:
            return Response({"detail": "taskId mismatch."}, status=400)

        apply_kie_result(job, payload)
        return Response({"detail": "ok"}, status=200)
