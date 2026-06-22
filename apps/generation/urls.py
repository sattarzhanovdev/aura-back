from django.urls import path

from .views import CreateGenerationJobView, GenerationJobDetailView

urlpatterns = [
    path("jobs/", CreateGenerationJobView.as_view(), name="generation-jobs"),
    path("jobs/<int:pk>/", GenerationJobDetailView.as_view(), name="generation-job-detail"),
]
