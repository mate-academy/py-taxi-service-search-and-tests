from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.assertEqual(str(manufacturer), "Test Manufacturer Test Country")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="password",
            first_name="first",
            last_name="last",
        )
        self.assertEqual(str(driver), "username (first last)")

    def test_car_str(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer", country="Test Country"
            ),
        )
        self.assertEqual(str(car), "Test Model")

    def test_driver_license_number(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="password",
            first_name="first",
            last_name="last",
            license_number="AAA12345",
        )
        self.assertEqual(driver.first_name, "first")
        self.assertEqual(driver.last_name, "last")
        self.assertEqual(driver.license_number, "AAA12345")
        self.assertTrue(driver.check_password("password"))
