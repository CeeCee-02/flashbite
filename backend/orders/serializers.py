from rest_framework import serializers
from .models import Order, OrderItem
from foods.models import FoodItem
from restaurants.models import Restaurant


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "food_item", "item_name", "unit_price", "quantity", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    rider_name = serializers.CharField(source="rider.full_name", read_only=True, default=None)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "restaurant",
            "restaurant_name",
            "rider",
            "rider_name",
            "delivery_address",
            "delivery_city",
            "delivery_latitude",
            "delivery_longitude",
            "customer_phone",
            "notes",
            "items_total",
            "delivery_fee",
            "grand_total",
            "status",
            "payment_status",
            "payment_reference",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "customer",
            "rider",
            "items_total",
            "delivery_fee",
            "grand_total",
            "status",
            "payment_status",
            "created_at",
            "updated_at",
        ]


class CreateOrderItemInputSerializer(serializers.Serializer):
    food_item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderInputSerializer(serializers.Serializer):
    restaurant_id = serializers.UUIDField()
    delivery_address = serializers.CharField()
    customer_phone = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
    items = CreateOrderItemInputSerializer(many=True)
