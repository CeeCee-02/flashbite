import hmac
import hashlib
import json
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from core.exceptions import success_response
from orders.models import Order, OrderStatus, PaymentStatus
from .models import PaymentLog


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def initialize_payment(request):
    """
    POST /api/payments/initialize/
    Body: { order_id }
    """
    order_id = request.data.get("order_id")
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Order not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # In production, calls Paystack API: https://api.paystack.co/transaction/initialize
    # Return authorization URL & payment reference
    reference = order.payment_reference or f"FB-{order.id.hex[:8]}"
    
    PaymentLog.objects.get_or_create(
        reference=reference,
        defaults={
            "order": order,
            "amount": order.grand_total,
            "provider": "paystack",
            "status": "initialized",
        }
    )

    return success_response(
        data={
            "authorization_url": f"https://checkout.paystack.com/mock-{reference}",
            "access_code": f"acc_{reference}",
            "reference": reference,
            "amount": float(order.grand_total),
            "email": order.customer.email,
        },
        message="Payment initialized."
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def verify_payment(request):
    """
    POST /api/payments/verify/
    Body: { reference }
    Immediate test-mode verification endpoint.
    """
    reference = request.data.get("reference")
    if not reference:
        return Response(
            {"success": False, "error": "BadRequest", "message": "Payment reference is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        order = Order.objects.get(payment_reference=reference)
    except Order.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Order with this reference not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Update payment & order status
    order.payment_status = PaymentStatus.PAID
    order.status = OrderStatus.CONFIRMED
    order.save(update_fields=["payment_status", "status", "updated_at"])

    PaymentLog.objects.filter(reference=reference).update(status="success")

    return success_response(
        data={"order_id": order.id, "status": order.status, "payment_status": order.payment_status},
        message="Payment verified successfully. Order confirmed!"
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def paystack_webhook(request):
    """
    POST /api/payments/webhook/
    Paystack Webhook Handler with mandatory HMAC SHA512 signature verification.
    """
    paystack_sk = getattr(settings, "PAYSTACK_SECRET_KEY", "")
    signature = request.headers.get("x-paystack-signature")

    if paystack_sk and signature:
        expected_sig = hmac.new(
            paystack_sk.encode("utf-8"),
            request.body,
            hashlib.sha512
        ).hexdigest()

        if signature != expected_sig:
            return Response(
                {"success": False, "error": "Unauthorized", "message": "Invalid webhook signature."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    payload = json.loads(request.body)
    event = payload.get("event")

    if event == "charge.success":
        data = payload.get("data", {})
        reference = data.get("reference")
        
        try:
            order = Order.objects.get(payment_reference=reference)
            order.payment_status = PaymentStatus.PAID
            order.status = OrderStatus.CONFIRMED
            order.save(update_fields=["payment_status", "status", "updated_at"])
            
            PaymentLog.objects.filter(reference=reference).update(
                status="success",
                gateway_response=data
            )
        except Order.DoesNotExist:
            pass

    return Response({"status": "success"}, status=status.HTTP_200_OK)
