from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="Bob",
            last_name="Smith",
        )
        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        car = Car.objects.create(
            model="Mitsubishi Eclipse",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_driver_license_number(self):
        username = "test"
        password = "test3434"
        license_number = "JIM26556"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
