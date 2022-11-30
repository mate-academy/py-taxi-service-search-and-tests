from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Country"
        )
        self.assertEqual(str(manufacturer),
                         "Name Country")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="username",
            last_name="last_name",
            first_name="first_name",
            password="password"
        )
        self.assertEqual(str(driver),
                         "username (first_name last_name)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Country"
        )
        car = Car.objects.create(
            model="model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "model")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="password",
            license_number="license_number"
        )
        self.assertEqual(driver.username, "username")
        self.assertTrue(driver.check_password("password"))
        self.assertEqual(driver.license_number, "license_number")
