from django.urls import path
from .views import order_list_create, order_detail, update_order_status

app_name = "orders"

urlpatterns = [
    path("", order_list_create, name="list-create"),
    path("<uuid:pk>/", order_detail, name="detail"),
    path("<uuid:pk>/status/", update_order_status, name="update-status"),
]
