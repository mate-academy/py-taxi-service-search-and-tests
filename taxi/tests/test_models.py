from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        self.driver = get_user_model().objects.create_user(
            username="test_name",
            password="test_password",
            license_number="test_license",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_create_driver_with_license(self) -> None:
        self.assertEqual(self.driver.username, "test_name")
        self.assertTrue(self.driver.check_password("test_password"))
        self.assertEqual(self.driver.license_number, "test_license")

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), str(self.car.model))
