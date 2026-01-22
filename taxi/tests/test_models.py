from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.driver = get_user_model().objects.create(
            username="driveruser",
            password="testpass",
            first_name="Test",
            last_name="Driver",
            license_number="TST12345"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Ford USA")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "driveruser (Test Driver)")

    def test_car_str(self):
        car = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "Mustang")

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.license_number, "TST12345")
