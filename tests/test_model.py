from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2"
        )
        self.assertEqual(str(manufacturer), "test2 test2")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test1",
            password="test12345",
            first_name="Test first",
            last_name="Test last",

        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), "test")

    def test_create_driver_with_license(self):
        driver = get_user_model().objects.create_user(
            username="test1",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            license_number="test12345",
        )
        self.assertEqual(driver.license_number, "test12345")
