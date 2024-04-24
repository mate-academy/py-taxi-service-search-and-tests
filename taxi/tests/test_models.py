from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(
            str(user),
            f"{user.username} ({user.first_name} {user.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        car = Car.objects.create(model="BMW X5", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
