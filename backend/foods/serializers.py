from rest_framework import serializers
from .models import FoodCategory, FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image_url",
            "is_available",
            "is_vegetarian",
            "is_spicy",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class FoodCategorySerializer(serializers.ModelSerializer):
    items = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = FoodCategory
        fields = [
            "id",
            "restaurant",
            "name",
            "description",
            "display_order",
            "items",
        ]
        read_only_fields = ["id"]
