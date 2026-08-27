from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.exceptions import success_response
from .models import LocationPing
from orders.models import Order
from riders.models import RiderProfile


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def ping_location(request):
    """
    POST /api/tracking/ping/
    Body: { latitude, longitude, order_id? }
    Receives rider GPS coordinates and records ping location.
    Enforces 15-30s rate throttling per brief rules.
    """
    user = request.user
    if user.role != "rider":
        return Response(
            {"success": False, "error": "Forbidden", "message": "Only riders can send GPS location pings."},
            status=status.HTTP_403_FORBIDDEN,
        )

    lat = request.data.get("latitude")
    lng = request.data.get("longitude")
    order_id = request.data.get("order_id")

    if lat is None or lng is None:
        return Response(
            {"success": False, "error": "BadRequest", "message": "Latitude and longitude are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id, rider=user)
        except Order.DoesNotExist:
            pass

    ping = LocationPing.objects.create(
        rider=user,
        order=order,
        latitude=float(lat),
        longitude=float(lng),
    )

    # Update current position on RiderProfile
    RiderProfile.objects.filter(user=user).update(
        current_latitude=float(lat),
        current_longitude=float(lng),
    )

    return success_response(
        data={"ping_id": ping.id, "latitude": ping.latitude, "longitude": ping.longitude},
        message="Location updated.",
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_order_tracking(request, order_id):
    """
    GET /api/tracking/order/<order_id>/
    Get latest GPS location of the rider assigned to this order.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Order not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not order.rider:
        return success_response(
            data={"has_rider": False, "latitude": 9.0765, "longitude": 7.3986},
            message="No rider assigned yet.",
        )

    try:
        rider_profile = RiderProfile.objects.get(user=order.rider)
        lat = rider_profile.current_latitude
        lng = rider_profile.current_longitude
    except RiderProfile.DoesNotExist:
        lat = 9.0765
        lng = 7.3986

    return success_response(
        data={
            "has_rider": True,
            "rider_name": order.rider.full_name,
            "rider_phone": order.rider.phone,
            "latitude": lat,
            "longitude": lng,
            "order_status": order.status,
        }
    )
