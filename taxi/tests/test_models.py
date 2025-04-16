from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.driver_data = {
            "username": "test",
            "license_number": "ABC54321",
            "password": "test123"
        }

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username=self.driver_data["username"],
            password=self.driver_data["password"]
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        new_car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer
        )
        self.assertEqual(
            str(new_car),
            new_car.model
        )

    def test_driver_license_number(self):
        driver_with_license = get_user_model().objects.create_user(
            username=self.driver_data["username"],
            license_number=self.driver_data["license_number"],
            password=self.driver_data["password"]
        )
        self.assertEqual(
            driver_with_license.license_number,
            self.driver_data["license_number"]
        )
        self.assertEqual(
            driver_with_license.username,
            self.driver_data["username"]
        )
        self.assertTrue(
            driver_with_license.check_password(self.driver_data["password"])
        )
