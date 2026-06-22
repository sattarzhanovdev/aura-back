from django.urls import path

from .views import CategoryListView, ClothingItemDetailView, ClothingItemListCreateView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="wardrobe-categories"),
    path("items/", ClothingItemListCreateView.as_view(), name="wardrobe-items"),
    path("items/<int:pk>/", ClothingItemDetailView.as_view(), name="wardrobe-item-detail"),
]
