from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class Model(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BingChilling",
            country="China"
        )
        self.car = Car.objects.create(
            model="test_model_car",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="riceman",
            password="ChinaIsTheBest",
            first_name="BimBim",
            last_name="BamBam",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} "
            f"{self.manufacturer.country}"
        )

    def test_car_str(self) -> None:
        self.assertEqual(
            str(self.car), self.car.model
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
