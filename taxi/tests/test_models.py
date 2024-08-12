from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.assertEqual(str(manufacturer), "Test Manufacturer Test Country")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test",
            password="Test123",
            email="<EMAIL>",
            first_name="Test_first",
            last_name="Test_last",
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} "
                         f"{driver.last_name})")

    def test_driver_create(self):
        username = "test"
        password = "79asdsas"
        license_number = "ABC98765"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "Test Car")
