from django.db import models
from django.conf import settings
from core.models import BaseModel
from restaurants.models import Restaurant
from foods.models import FoodItem


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending Confirmation"
    CONFIRMED = "confirmed", "Order Confirmed"
    PREPARING = "preparing", "Preparing Food"
    READY = "ready", "Ready for Pickup"
    PICKED_UP = "picked_up", "Picked Up by Rider"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending Payment"
    PAID = "paid", "Payment Verified"
    FAILED = "failed", "Payment Failed"


class Order(BaseModel):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_orders",
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rider_deliveries",
    )
    
    delivery_address = models.CharField(max_length=255)
    delivery_city = models.CharField(max_length=100, default="Abuja")
    delivery_latitude = models.FloatField(default=9.0765)
    delivery_longitude = models.FloatField(default=7.3986)
    customer_phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    
    items_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )
    payment_reference = models.CharField(max_length=100, blank=True, unique=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{str(self.id)[:8]} - {self.customer.full_name} ({self.status})"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.SET_NULL,
        null=True,
    )
    item_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"
