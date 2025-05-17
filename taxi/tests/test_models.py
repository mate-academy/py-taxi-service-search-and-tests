from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self):
        self.username = "test_driver"
        self.password = "test123"
        self.license_number = "test_license"
        self.first_name = "test_first_name"
        self.last_name = "test_last_name"
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            license_number=self.license_number,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.manufacturer = Manufacturer(
            name="test name",
            country="test country",
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
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        car = Car(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_driver_fields(self):
        self.assertEqual(self.driver.first_name, self.first_name)
        self.assertEqual(self.driver.last_name, self.last_name)
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertEqual(self.driver.username, self.username)
        self.assertTrue(self.driver.check_password(self.password))
