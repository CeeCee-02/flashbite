from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant
from foods.models import FoodCategory, FoodItem
from riders.models import RiderProfile, VerificationStatus

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with authentic Nigerian restaurants, food menus, and sample users."

    def handle(self, *args, **options):
        self.stdout.write("Seeding FLASHBITE database...")

        # 1. Create Restaurant Owner Users & Restaurants
        restaurants_data = [
            {
                "email": "owner.mamacass@flashbite.ng",
                "name": "Mama Cass Jollof & Grill",
                "slug": "mama-cass-jollof",
                "description": "Authentic smoky party Jollof rice, fried plantains, grilled chicken, and traditional Nigerian swallows.",
                "address": "Plot 1042 Ahmadu Bello Way, Area 11, Garki",
                "city": "Abuja",
                "phone": "08031112233",
                "logo_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500&q=80",
                "banner_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&q=80",
                "rating": 4.8,
                "categories": [
                    {
                        "name": "Jollof & Rice Specials",
                        "items": [
                            {"name": "Smoky Party Jollof & Chicken", "price": 4500, "desc": "Smoky firewood Jollof served with crispy fried chicken and fried plantains.", "image": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=500&q=80"},
                            {"name": "Special Fried Rice & Peppered Turkey", "price": 5200, "desc": "Wok-fried vegetable rice topped with tender peppered turkey.", "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=500&q=80"},
                            {"name": "Ofada Rice & Ayamase Stew", "price": 4800, "desc": "Local unpolished Ofada rice with authentic green pepper Ayamase stew, boiled egg and fried beef.", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80"},
                        ]
                    },
                    {
                        "name": "Proteins & Extras",
                        "items": [
                            {"name": "Peppered Beef Skewer", "price": 2000, "desc": "Spicy habanero glazed beef chunk.", "image": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=500&q=80"},
                            {"name": "Fried Dodo (Plantain)", "price": 1000, "desc": "Sweet golden ripe fried plantains.", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80"},
                        ]
                    }
                ]
            },
            {
                "email": "owner.suya@flashbite.ng",
                "name": "Suya Kingdom Abuja",
                "slug": "suya-kingdom-abuja",
                "description": "Authentic Northern Nigerian beef & ram suya, masa, and spicy Kilishi.",
                "address": "Zone 4 Pepper Street, Wuse 2",
                "city": "Abuja",
                "phone": "08054445566",
                "logo_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80",
                "banner_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1200&q=80",
                "rating": 4.9,
                "categories": [
                    {
                        "name": "Suya Delicacies",
                        "items": [
                            {"name": "Special Beef Suya (Full Portion)", "price": 3500, "desc": "Thinly sliced tender beef grilled over charcoal with Yaji spice, onions, and cabbage.", "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80"},
                            {"name": "Ram Suya Platter", "price": 4500, "desc": "Juicy ram meat suya marinated with Northern spices.", "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80"},
                            {"name": "Chicken Suya", "price": 3800, "desc": "Boneless grilled chicken breast sprinkled with hot Yaji powder.", "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=500&q=80"},
                        ]
                    }
                ]
            },
            {
                "email": "owner.burgers@flashbite.ng",
                "name": "Metropolitan Gourmet Burgers",
                "slug": "metropolitan-burgers",
                "description": "Juicy smash burgers, crispy chicken wings, and loaded cheese fries.",
                "address": "12 Aminu Kano Crescent, Wuse 2",
                "city": "Abuja",
                "phone": "08089990011",
                "logo_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80",
                "banner_url": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=1200&q=80",
                "rating": 4.7,
                "categories": [
                    {
                        "name": "Smash Burgers",
                        "items": [
                            {"name": "Double Cheese Smash Burger", "price": 4200, "desc": "Two beef patties, cheddar cheese, pickles, and signature house sauce.", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80"},
                            {"name": "Crispy Zinger Chicken Burger", "price": 3900, "desc": "Buttermilk fried chicken breast, spicy mayo, and crunchy slaw.", "image": "https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=500&q=80"},
                        ]
                    },
                    {
                        "name": "Sides & Drinks",
                        "items": [
                            {"name": "Loaded Cheese Fries", "price": 2200, "desc": "Crispy french fries drenched in warm cheddar sauce and jalapenos.", "image": "https://images.unsplash.com/photo-1585109649139-366815a0d713?w=500&q=80"},
                            {"name": "Chilled Zobo Drink (500ml)", "price": 800, "desc": "Fresh hibiscus infusion with ginger and pineapple juice.", "image": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500&q=80"},
                        ]
                    }
                ]
            }
        ]

        for r_data in restaurants_data:
            user, _ = User.objects.get_or_create(
                email=r_data["email"],
                defaults={
                    "full_name": f"Manager ({r_data['name']})",
                    "role": "restaurant",
                    "is_active": True,
                }
            )
            user.set_password("Str0ng!Pass99")
            user.save()

            restaurant, _ = Restaurant.objects.get_or_create(
                slug=r_data["slug"],
                defaults={
                    "owner": user,
                    "name": r_data["name"],
                    "description": r_data["description"],
                    "address": r_data["address"],
                    "city": r_data["city"],
                    "phone": r_data["phone"],
                    "logo_url": r_data["logo_url"],
                    "banner_url": r_data["banner_url"],
                    "rating": r_data["rating"],
                }
            )

            for cat_data in r_data["categories"]:
                category, _ = FoodCategory.objects.get_or_create(
                    restaurant=restaurant,
                    name=cat_data["name"],
                )

                for item_data in cat_data["items"]:
                    FoodItem.objects.get_or_create(
                        category=category,
                        name=item_data["name"],
                        defaults={
                            "price": item_data["price"],
                            "description": item_data["desc"],
                            "image_url": item_data["image"],
                            "is_available": True,
                        }
                    )

        # 2. Create Sample Rider User & Profile
        rider_user, _ = User.objects.get_or_create(
            email="rider.musa@flashbite.ng",
            defaults={
                "full_name": "Musa Ibrahim",
                "phone": "08077889900",
                "role": "rider",
                "is_active": True,
            }
        )
        rider_user.set_password("Str0ng!Pass99")
        rider_user.save()

        RiderProfile.objects.get_or_create(
            user=rider_user,
            defaults={
                "vehicle_type": "motorcycle",
                "vehicle_plate": "ABJ-492-KY",
                "verification_status": VerificationStatus.VERIFIED,
                "is_available": True,
            }
        )

        # 3. Create Sample Customer User
        customer_user, _ = User.objects.get_or_create(
            email="customer.demola@flashbite.ng",
            defaults={
                "full_name": "Demola Adebayo",
                "phone": "08011223344",
                "role": "customer",
                "is_active": True,
            }
        )
        customer_user.set_password("Str0ng!Pass99")
        customer_user.save()

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with authentic restaurants and menus!"))
