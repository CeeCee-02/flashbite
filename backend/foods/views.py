from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from core.exceptions import success_response
from .models import FoodCategory, FoodItem
from .serializers import FoodCategorySerializer, FoodItemSerializer
from restaurants.models import Restaurant


class FoodCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "restaurant_profile"):
            return FoodCategory.objects.filter(restaurant=user.restaurant_profile)
        return FoodCategory.objects.none()

    def perform_create(self, serializer):
        restaurant = self.request.user.restaurant_profile
        serializer.save(restaurant=restaurant)


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "restaurant_profile"):
            return FoodItem.objects.filter(category__restaurant=user.restaurant_profile)
        return FoodItem.objects.none()
