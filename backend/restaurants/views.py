from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.exceptions import success_response
from .models import Restaurant
from .serializers import RestaurantSerializer
from foods.serializers import FoodCategorySerializer
from foods.models import FoodCategory


class PublicRestaurantListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class PublicRestaurantDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        categories = FoodCategory.objects.filter(restaurant=instance).prefetch_related("items")
        category_serializer = FoodCategorySerializer(categories, many=True)
        
        data = serializer.data
        data["categories"] = category_serializer.data
        return success_response(data=data)


@api_view(["GET", "POST", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def restaurant_me_profile(request):
    user = request.user
    if user.role != "restaurant":
        return Response(
            {"success": False, "error": "Forbidden", "message": "Only restaurant owners can access this endpoint."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        restaurant = Restaurant.objects.get(owner=user)
    except Restaurant.DoesNotExist:
        restaurant = None

    if request.method == "GET":
        if not restaurant:
            return Response(
                {"success": False, "error": "NotFound", "message": "No restaurant profile created yet."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = RestaurantSerializer(restaurant)
        return success_response(data=serializer.data)

    if request.method in ["POST", "PATCH"]:
        if restaurant:
            serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        else:
            serializer = RestaurantSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        if not restaurant:
            name = serializer.validated_data.get("name", "Restaurant")
            slug = name.lower().replace(" ", "-") + f"-{user.id.hex[:4]}"
            restaurant = serializer.save(owner=user, slug=slug)
        else:
            restaurant = serializer.save()

        return success_response(data=RestaurantSerializer(restaurant).data, message="Restaurant profile saved.")
