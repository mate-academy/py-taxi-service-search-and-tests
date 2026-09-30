from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelStrTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test.user",
            password="test12345",
            first_name="Test",
            last_name="User",
            license_number="TES12345",
        )
        self.assertEqual(str(driver), "test.user (Test User)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")


class DriverModelTests(TestCase):
    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test.user",
            password="test12345",
            license_number="TES12345",
        )
        self.assertEqual(driver.license_number, "TES12345")
