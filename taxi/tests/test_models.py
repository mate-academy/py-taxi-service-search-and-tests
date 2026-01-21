from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X7",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class DriverModelsTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="ben",
            password="qwerty123",
            first_name="Ben",
            last_name="Qwe",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "ben"
        password = "qwerty123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="ben",
            password="qwerty123",
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
