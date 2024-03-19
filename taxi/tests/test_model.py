from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country")
        self.assertEqual(str(manufacturer),
                         "Test manufacturer Test country")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country")
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer)
        self.assertEqual(str(car), "Test model")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Test driver",
            first_name="Test first name",
            last_name="Test last name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_has_license_number(self):
        username = "test"
        password = "test123"
        license_number = "GEP12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
