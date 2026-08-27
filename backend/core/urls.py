"""Health check endpoint for Render's uptime monitor."""

from django.urls import path
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([])
def health_check(request):
    return Response({"status": "ok", "service": "flashbite-api"})


urlpatterns = [
    path("", health_check, name="health-check"),
]
