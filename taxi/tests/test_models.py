from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="TestCountry"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="TestCountry"
        )
        model = "VX35"
        car = Car.objects.create(
            model=model, manufacturer=manufacturer
        )
        self.assertEqual(str(car), model)


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.license_number = "TES12345"
        self.driver = get_user_model().objects.create(
            username="test",
            password="testPass1",
            license_number=self.license_number
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            (f"{self.driver.username} "
             f"({self.driver.first_name} {self.driver.last_name})")
        )

    def test_driver_license_number(self):
        self.assertEqual(self.driver.license_number, self.license_number)
