from django.urls import path

from .views import OutfitDetailView, SuggestOutfitView

urlpatterns = [
    path("suggest/", SuggestOutfitView.as_view(), name="outfits-suggest"),
    path("<int:pk>/", OutfitDetailView.as_view(), name="outfit-detail"),
]
