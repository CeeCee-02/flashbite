from django.urls import path
from .views import ping_location, get_order_tracking

app_name = "tracking"

urlpatterns = [
    path("ping/", ping_location, name="ping"),
    path("order/<uuid:order_id>/", get_order_tracking, name="order-tracking"),
]
