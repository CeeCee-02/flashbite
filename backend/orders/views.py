import uuid
from decimal import Decimal
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.exceptions import success_response
from .models import Order, OrderItem, OrderStatus, PaymentStatus
from .serializers import OrderSerializer, CreateOrderInputSerializer
from restaurants.models import Restaurant
from foods.models import FoodItem


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def order_list_create(request):
    user = request.user

    if request.method == "GET":
        # Role-based filtering
        if user.role == "customer":
            orders = Order.objects.filter(customer=user).prefetch_related("items", "restaurant")
        elif user.role == "restaurant" and hasattr(user, "restaurant_profile"):
            orders = Order.objects.filter(restaurant=user.restaurant_profile).prefetch_related("items", "customer")
        elif user.role == "rider":
            orders = Order.objects.filter(rider=user).prefetch_related("items", "restaurant", "customer")
        else:
            orders = Order.objects.all().prefetch_related("items", "restaurant", "customer")

        serializer = OrderSerializer(orders, many=True)
        return success_response(data=serializer.data)

    if request.method == "POST":
        input_serializer = CreateOrderInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        try:
            restaurant = Restaurant.objects.get(id=data["restaurant_id"])
        except Restaurant.DoesNotExist:
            return Response(
                {"success": False, "error": "NotFound", "message": "Restaurant not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        items_data = data["items"]
        items_total = Decimal("0.00")
        order_items_to_create = []

        for item_input in items_data:
            try:
                food_item = FoodItem.objects.get(id=item_input["food_item_id"])
            except FoodItem.DoesNotExist:
                return Response(
                    {"success": False, "error": "NotFound", "message": f"Food item {item_input['food_item_id']} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            qty = item_input["quantity"]
            subtotal = food_item.price * qty
            items_total += subtotal

            order_items_to_create.append({
                "food_item": food_item,
                "item_name": food_item.name,
                "unit_price": food_item.price,
                "quantity": qty,
                "subtotal": subtotal,
            })

        delivery_fee = Decimal("500.00")
        grand_total = items_total + delivery_fee
        pay_ref = f"FB-{uuid.uuid4().hex[:10].upper()}"

        order = Order.objects.create(
            customer=user,
            restaurant=restaurant,
            delivery_address=data["delivery_address"],
            customer_phone=data["customer_phone"],
            notes=data.get("notes", ""),
            items_total=items_total,
            delivery_fee=delivery_fee,
            grand_total=grand_total,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            payment_reference=pay_ref,
        )

        for item_dict in order_items_to_create:
            OrderItem.objects.create(order=order, **item_dict)

        return success_response(
            data=OrderSerializer(order).data,
            message="Order placed successfully. Proceed to payment.",
            status_code=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.prefetch_related("items", "restaurant", "customer", "rider").get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Order not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Security check: User must be customer, restaurant owner, or rider for this order
    user = request.user
    if (
        user != order.customer
        and (not hasattr(user, "restaurant_profile") or user.restaurant_profile != order.restaurant)
        and user != order.rider
        and user.role != "admin"
    ):
        return Response(
            {"success": False, "error": "Forbidden", "message": "You are not authorized to view this order."},
            status=status.HTTP_403_FORBIDDEN,
        )

    return success_response(data=OrderSerializer(order).data)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, pk):
    """
    PATCH /api/orders/<pk>/status/
    Body: { status: "preparing" | "ready" | "picked_up" | "delivered" | "cancelled" }
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Order not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    new_status = request.data.get("status")
    if new_status not in [choice[0] for choice in OrderStatus.choices]:
        return Response(
            {"success": False, "error": "BadRequest", "message": f"Invalid status: {new_status}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order.status = new_status
    order.save(update_fields=["status", "updated_at"])

    return success_response(data=OrderSerializer(order).data, message=f"Order status updated to {new_status}.")
