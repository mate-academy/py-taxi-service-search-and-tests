from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="BobMarley",
            first_name="Bob",
            last_name="Marley",
            password="qwerty12345",
            license_number="BMC12345",
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_licence_number(self) -> None:
        self.assertEqual(self.driver.license_number, "BMC12345")


class CarModelTest(TestCase):
    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry 3.5", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
