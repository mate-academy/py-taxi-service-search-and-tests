from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.username = "TestUser"
        self.first_name = "Test_firstname"
        self.last_name = "Test_last_name"
        self.license_number = "ABC12345"
        self.password = "test1234"

        self.manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )

        self.driver = get_user_model().objects.create_user(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            license_number=self.license_number

        )
        self.car = Car.objects.create(
            model="C200",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_string(self):
        self.assertEqual(str(self.manufacturer), "Mercedes Germany")

    def test_car_string(self):
        self.assertEqual(str(self.car), "C200")

    def test_driver_string(self):
        self.assertEqual(
            str(self.driver),
            f"{self.username} ({self.first_name} {self.last_name})"
            )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertTrue(self.driver.check_password(self.password))
        self.assertEqual(self.driver.license_number, self.license_number)
