from django.urls import path
from .views import PublicRestaurantListView, PublicRestaurantDetailView, restaurant_me_profile

app_name = "restaurants"

urlpatterns = [
    path("", PublicRestaurantListView.as_view(), name="list"),
    path("me/", restaurant_me_profile, name="me"),
    path("<slug:slug>/", PublicRestaurantDetailView.as_view(), name="detail"),
]
