from django.contrib.auth import get_user_model


def get_user_model_function():
    return get_user_model().objects.create_user(
        username="test_admin",
        password="1111111",
        license_number="AAA11111",
    )
