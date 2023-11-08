from django.contrib.auth import get_user_model


def get_user_model_function():
    return get_user_model().objects.create_user(
        username="driver",
        password="password1",
        license_number="ABC12345",
    )
