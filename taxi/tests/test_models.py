from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        model = "test",
        manufacturer = Manufacturer.objects.create(name="test")
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(
            str(car),
            f"{car.model}"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        license_number = "test_license_number"
        password = "test_password"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
