from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.exceptions import success_response
from .models import RiderProfile
from .serializers import RiderProfileSerializer
from orders.models import Order, OrderStatus
from orders.serializers import OrderSerializer


@api_view(["GET", "POST", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def rider_me_profile(request):
    user = request.user
    if user.role != "rider":
        return Response(
            {"success": False, "error": "Forbidden", "message": "Only riders can access this endpoint."},
            status=status.HTTP_403_FORBIDDEN,
        )

    profile, _ = RiderProfile.objects.get_or_create(user=user)

    if request.method == "GET":
        serializer = RiderProfileSerializer(profile)
        return success_response(data=serializer.data)

    if request.method in ["POST", "PATCH"]:
        serializer = RiderProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message="Rider profile updated.")


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def available_orders_feed(request):
    """
    GET /api/riders/available-orders/
    List orders that are READY for pickup and unassigned to any rider.
    """
    if request.user.role != "rider":
        return Response(
            {"success": False, "error": "Forbidden", "message": "Only riders can view available orders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    orders = Order.objects.filter(status=OrderStatus.READY, rider__isnull=True).prefetch_related("items", "restaurant", "customer")
    serializer = OrderSerializer(orders, many=True)
    return success_response(data=serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def accept_order(request, order_id):
    """
    POST /api/riders/accept-order/<order_id>/
    Assign rider to ready order.
    """
    user = request.user
    if user.role != "rider":
        return Response(
            {"success": False, "error": "Forbidden", "message": "Only riders can accept orders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        order = Order.objects.get(id=order_id, status=OrderStatus.READY, rider__isnull=True)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Order is not available for acceptance."},
            status=status.HTTP_404_NOT_FOUND,
        )

    order.rider = user
    order.save(update_fields=["rider", "updated_at"])

    return success_response(data=OrderSerializer(order).data, message="Order accepted! Proceed to restaurant for pickup.")
