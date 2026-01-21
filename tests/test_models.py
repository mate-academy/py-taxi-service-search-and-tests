from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car

username = "test_driver"
password = "test1234"
license_number = "AA123456"


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="Test",
            last_name="Driver",
            license_number=license_number
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password), password)
        self.assertEqual(driver.license_number, license_number)
