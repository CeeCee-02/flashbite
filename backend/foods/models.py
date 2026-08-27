from django.db import models
from core.models import BaseModel
from restaurants.models import Restaurant


class FoodCategory(BaseModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Food categories"
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class FoodItem(BaseModel):
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in NGN
    image_url = models.URLField(blank=True, default="")
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (₦{self.price})"
