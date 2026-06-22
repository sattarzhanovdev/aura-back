from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StylePreference
from .serializers import ProfileSerializer, ProfileUpdateSerializer, StylePreferenceSerializer


class StylePreferenceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StylePreferenceSerializer
    queryset = StylePreference.objects.all()


class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(ProfileSerializer(self.get_object()).data)


class ReferencePhotoUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        photo = request.FILES.get("reference_photo")
        if not photo:
            return Response({"detail": "reference_photo file is required."}, status=400)
        profile.reference_photo = photo
        profile.save()
        return Response(ProfileSerializer(profile).data)


class OnboardingCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        missing = []
        if not profile.body_type:
            missing.append("body_type")
        if not profile.reference_photo:
            missing.append("reference_photo")
        if not profile.style_preferences.exists():
            missing.append("style_preferences")
        if missing:
            return Response(
                {"detail": "Onboarding incomplete.", "missing_fields": missing},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        profile.onboarding_completed = True
        profile.save()
        return Response(ProfileSerializer(profile).data)
