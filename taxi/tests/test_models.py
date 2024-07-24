from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTestCase(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
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

    def test_driver_license_number(self):
        license_number = "test_license_number"
        password = "<PASSWORD>"
        username = "test_username"
        driver = get_user_model().objects.create_user(
            username="test_username",
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.username, username)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class DriverModelInvalidTests(TestCase):
    def test_create_driver_without_license_number(self):
        user = get_user_model()
        with self.assertRaises(ValidationError):
            driver = user(
                username="invalid_driver",
                password="test_pas123",
                first_name="Invalid",
                last_name="Driver",
                license_number="",
            )
            driver.full_clean()
            driver.save()
