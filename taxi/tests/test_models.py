from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TEST"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="TestDriver",
            password="test123456",
            first_name="TestFname",
            last_name="TestLname",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license_number(self) -> None:
        driver = get_user_model().objects.create_user(
            username="TestDriver",
            password="test123456",
            license_number="TES12345"
        )

        self.assertEqual(driver.username, "TestDriver")
        self.assertEqual(driver.license_number, "TES12345")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TEST"
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
