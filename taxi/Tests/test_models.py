from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(
            str(manufacturer),
            expected_str
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            email="<EMAIL>",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license(self):
        username = "test"
        license_number = "test_license_number"
        password = "test123"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
