from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_car_str(self):
        car_str = Car(model="tests")
        self.assertEqual(str(car_str), car_str.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test1"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        license_number = "Test License_number"
        driver = get_user_model().objects.create(
            username=username,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
