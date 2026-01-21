from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test2",
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_car_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test2",
        )
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="first test",
            last_name="last test",
        )
        car = Car.objects.create(
            model="ttt12",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test1234"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url(self):
        username = "test"
        password = "test1234"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

