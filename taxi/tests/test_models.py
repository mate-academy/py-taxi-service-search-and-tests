from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="AAA12345"
        )
        self.assertEqual(str(driver), "testuser (John Doe)")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(model="Mustang", manufacturer=manufacturer)
        self.assertEqual(str(car), "Mustang")
