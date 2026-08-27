"""
URL configuration for FLASHBITE backend.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # API schema + docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # App APIs
    path("api/auth/", include("accounts.urls")),
    path("api/restaurants/", include("restaurants.urls")),
    path("api/foods/", include("foods.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/riders/", include("riders.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/tracking/", include("tracking.urls")),
    path("api/notifications/", include("notifications.urls")),

    # Health check (used by Render)
    path("api/health/", include("core.urls")),
]
