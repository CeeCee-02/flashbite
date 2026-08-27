from django.urls import path
from .views import rider_me_profile, available_orders_feed, accept_order

app_name = "riders"

urlpatterns = [
    path("me/", rider_me_profile, name="me"),
    path("available-orders/", available_orders_feed, name="available-orders"),
    path("accept-order/<uuid:order_id>/", accept_order, name="accept-order"),
]
