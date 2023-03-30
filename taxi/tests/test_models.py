from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Name", country="Country"
        )
        self.car = Car.objects.create(
            model="Test", manufacturer=Manufacturer.objects.get(pk=1),
        )
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            license_number="ASD12345",
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f""f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, "driver")
        self.assertTrue(self.driver.check_password("driver12345"))
        self.assertEqual(self.driver.license_number, "ASD12345")

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
