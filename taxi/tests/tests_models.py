from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer", country="TestCountry"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_create_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "AAA12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="Test",
            last_name="Test",
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer", country="TestCountry"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)

        self.assertEqual(str(car), f"{car.model}")
