from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="strong_password",
            email="secreat_test_email@ukrnet.ua",
            license_number="DIR12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Banderomobile",
            country="Ukrainian_Empire"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer), f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test_model",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_all_information(self):
        username = "test_username"
        first_name = "test_first_name"
        last_name = "test_last_name"
        password = "strong_password"
        email = "secreat_test_email@ukrnet.ua"
        license_number = "DIR12345"

        self.assertEqual(self.driver.username, username)
        self.assertEqual(self.driver.first_name, first_name)
        self.assertEqual(self.driver.last_name, last_name)
        self.assertEqual(self.driver.email, email)
        self.assertEqual(self.driver.license_number, license_number)
        self.assertTrue(self.driver.check_password(password))
