from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first name",
            last_name="Test last name"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

    def test_manugacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test car",
            manufacturer=self.manufacturer,
        )

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_license_number(self):
        username = "test username"
        password = "test12345"
        license_number = "Test license number"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        self.assertEquals(self.driver.get_absolute_url(), "/drivers/1/")
