from rest_framework import generics, permissions

from .models import Category, ClothingItem
from .serializers import CategorySerializer, ClothingItemSerializer


class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ClothingItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClothingItemSerializer

    def get_queryset(self):
        qs = ClothingItem.objects.filter(user=self.request.user, is_active=True)
        category_slug = self.request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClothingItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClothingItemSerializer

    def get_queryset(self):
        return ClothingItem.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
