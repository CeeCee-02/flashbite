from django.db import models
from django.conf import settings
from core.models import BaseModel


class VerificationStatus(models.TextChoices):
    PENDING = "pending", "Pending Verification"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


class RiderProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rider_profile",
        limit_choices_to={"role": "rider"},
    )
    vehicle_type = models.CharField(
        max_length=50,
        choices=[("motorcycle", "Motorcycle"), ("bicycle", "Bicycle"), ("car", "Car")],
        default="motorcycle",
    )
    vehicle_plate = models.CharField(max_length=20, blank=True)
    driver_license_number = models.CharField(max_length=50, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.VERIFIED,  # Auto-verified for bootstrap MVP
    )
    is_available = models.BooleanField(default=True)
    current_latitude = models.FloatField(default=9.0765)
    current_longitude = models.FloatField(default=7.3986)

    def __str__(self):
        return f"Rider: {self.user.full_name} ({self.vehicle_type})"
