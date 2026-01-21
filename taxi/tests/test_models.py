from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test12345",

        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_driver_create_with_license(self):
        username = "test_username"
        password = "test_12345"
        license_number = "test_license"
        driver = get_user_model().objects.create_user(
            first_name="test First",
            last_name="test Last",
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
