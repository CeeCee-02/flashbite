from django.db import models
from core.models import BaseModel
from orders.models import Order


class PaymentLog(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payment_logs",
    )
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=50, default="paystack")
    status = models.CharField(max_length=50, default="pending")
    gateway_response = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Payment {self.reference} ({self.status})"
