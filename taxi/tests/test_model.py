from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        driver = Driver.objects.create(
            username="test_user",
            license_number="QWE12345"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_user",
            password="password123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_licence_number(self):
        username = "test_user"
        password = "password123"
        license_number = "QWE12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
