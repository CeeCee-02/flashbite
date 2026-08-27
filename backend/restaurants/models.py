from django.db import models
from django.conf import settings
from core.models import BaseModel


class Restaurant(BaseModel):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="restaurant_profile",
        limit_choices_to={"role": "restaurant"},
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default="Abuja")
    state = models.CharField(max_length=100, default="FCT")
    phone = models.CharField(max_length=20)
    logo_url = models.URLField(blank=True, default="")
    banner_url = models.URLField(blank=True, default="")
    latitude = models.FloatField(default=9.0765)
    longitude = models.FloatField(default=7.3986)
    is_open = models.BooleanField(default=True)
    prep_time_minutes = models.IntegerField(default=25)
    rating = models.FloatField(default=4.5)

    class Meta:
        ordering = ["-rating", "-created_at"]

    def __str__(self):
        return self.name
