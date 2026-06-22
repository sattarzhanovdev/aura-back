from django.urls import path

from .onboarding_views import (
    OnboardingCompleteView,
    ProfileUpdateView,
    ReferencePhotoUploadView,
    StylePreferenceListView,
)

urlpatterns = [
    path("style-preferences/", StylePreferenceListView.as_view(), name="onboarding-style-preferences"),
    path("profile/", ProfileUpdateView.as_view(), name="onboarding-profile"),
    path("reference-photo/", ReferencePhotoUploadView.as_view(), name="onboarding-reference-photo"),
    path("complete/", OnboardingCompleteView.as_view(), name="onboarding-complete"),
]
