from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    username = "test_user"
    password = "test_password"
    license_number = "ABC123"

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="John",
            last_name="Doe",
            license_number=self.license_number,
        )
        self.car = Car.objects.create(model="test", manufacturer=self.manufacturer)
        self.car.drivers.set([self.driver])

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} " f"{self.manufacturer.country}",
        )

    def test_driver_create_with_license_number(self):
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_driver_username(self):
        self.assertEqual(self.driver.username, self.username)

    def test_driver_password(self):
        self.assertTrue(self.driver.check_password(self.password))

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "test")
