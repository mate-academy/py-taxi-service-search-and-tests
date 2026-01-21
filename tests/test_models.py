from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.driver = Driver.objects.create_user(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            password="password123",
            license_number="ABC1234",
        )

        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
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
