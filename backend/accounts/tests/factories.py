"""
accounts/tests/factories.py
Factory Boy factories for test data generation.
"""

import factory
from django.contrib.auth import get_user_model

from accounts.models import EmailVerificationToken, PasswordResetToken, UserRole

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker("name")
    phone = factory.Faker("phone_number")
    role = UserRole.CUSTOMER
    is_active = True  # active by default for most tests
    password = factory.PostGenerationMethodCall("set_password", "Str0ng!Pass")


class InactiveUserFactory(UserFactory):
    is_active = False


class RestaurantUserFactory(UserFactory):
    role = UserRole.RESTAURANT


class RiderUserFactory(UserFactory):
    role = UserRole.RIDER


class AdminUserFactory(UserFactory):
    role = UserRole.ADMIN
    is_staff = True
    is_superuser = True


class EmailVerificationTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailVerificationToken

    user = factory.SubFactory(InactiveUserFactory)


class PasswordResetTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PasswordResetToken

    user = factory.SubFactory(UserFactory)
