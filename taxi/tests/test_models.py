from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Testland"
        )

        self.assertEqual(str(manufacturer), "Test Testland")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="user123",
            first_name="Test",
            last_name="Tester"
        )

        self.assertEqual(str(driver), "test_user (Test Tester)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Testland"
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), "test model")

    def test_create_driver_with_license_number(self):
        username = "test_user"
        password = "user123"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
