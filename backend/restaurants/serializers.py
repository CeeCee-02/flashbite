from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "address",
            "city",
            "state",
            "phone",
            "logo_url",
            "banner_url",
            "latitude",
            "longitude",
            "is_open",
            "prep_time_minutes",
            "rating",
            "owner_name",
            "created_at",
        ]
        read_only_fields = ["id", "rating", "created_at"]
