from rest_framework import serializers
from .models import RiderProfile


class RiderProfileSerializer(serializers.ModelSerializer):
    rider_name = serializers.CharField(source="user.full_name", read_only=True)
    rider_phone = serializers.CharField(source="user.phone", read_only=True)
    rider_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = RiderProfile
        fields = [
            "id",
            "rider_name",
            "rider_phone",
            "rider_email",
            "vehicle_type",
            "vehicle_plate",
            "driver_license_number",
            "verification_status",
            "is_available",
            "current_latitude",
            "current_longitude",
            "created_at",
        ]
        read_only_fields = ["id", "verification_status", "created_at"]
