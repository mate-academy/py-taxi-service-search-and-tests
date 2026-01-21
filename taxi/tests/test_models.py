from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="pididi",
            first_name="Pididi",
            last_name="P"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "pididi"
        license_number = "ASD56565"
        password = "123asd"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )
