from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="USA"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Mercedes S-class",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver(self):
        username = "Bob123"
        password = "Test123"
        first_name = "Bob"
        last_name = "Bobul"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(
            driver.license_number,
            license_number
        )
        self.assertTrue(
            driver.check_password(password)
        )
