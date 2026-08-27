from django.db import models
from django.conf import settings
from core.models import BaseModel
from orders.models import Order


class LocationPing(BaseModel):
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="location_pings",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tracking_pings",
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rider.email} ({self.latitude}, {self.longitude})"
