from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="FormulaUA",
            country="Ukraine",
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="username",
            password="iliketotest",
            first_name="firstname",
            last_name="lastname",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "FormulaUA Ukraine")

    def test_car_str(self):
        self.assertEqual(str(self.car), "TestModel")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "username (firstname lastname)")

    def test_driver_with_license_number(self):
        self.assertEqual(self.driver.license_number, "ABC12345")
        self.assertTrue(self.driver.check_password("iliketotest"))


