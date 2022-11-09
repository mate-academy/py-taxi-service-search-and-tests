from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="test"
        )

        self.username = "test.test"
        self.password = "test12345"
        self.license_number = "TES12345"
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.license_number,
            last_name="test_last",
            license_number="TES12345",
        )

        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertTrue(self.driver.check_password(self.password))
        self.assertEqual(self.driver.license_number, self.license_number)
