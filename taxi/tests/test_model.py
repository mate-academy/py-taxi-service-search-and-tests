from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_model(self):
        username = "test_username"
        first_name = "test_first"
        last_name = "test_last"
        license_number = "ABC12345"
        password = "test123"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            password=password,
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        car = Car.objects.create(
            manufacturer=manufacturer,
            model="test_model",
        )

        self.assertEqual(str(car), car.model)
