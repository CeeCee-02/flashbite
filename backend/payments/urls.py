from django.urls import path
from .views import initialize_payment, verify_payment, paystack_webhook

app_name = "payments"

urlpatterns = [
    path("initialize/", initialize_payment, name="initialize"),
    path("verify/", verify_payment, name="verify"),
    path("webhook/", paystack_webhook, name="webhook"),
]
