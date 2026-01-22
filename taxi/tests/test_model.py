from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

        self.driver = get_user_model().objects.create(
            username="testdriver",
            password="testpassword",
            license_number="QWE12345",
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(str(self.manufacturer), "Honda Japan")

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), "Camry")

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_creation_with_license_number(self) -> None:
        self.assertEqual(self.driver.license_number, "QWE12345")
