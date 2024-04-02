from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_format_str(self):
        manufacturer_format = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer_format),
            f"{manufacturer_format.name} {manufacturer_format.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        license_number = "AQS12345"
        username = "test"
        password = "test1234"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url_driver(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )

    def test_car_str(self):
        manufacturer_format = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="test_first",
            last_name="test_last",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer_format,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)
