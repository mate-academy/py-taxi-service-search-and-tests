from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="Testpasswd",
            first_name="Test first",
            last_name="Test last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        driver = get_user_model().objects.create_user(
            username="Test",
            password="Testpasswd",
            first_name="Test first",
            last_name="Test last",
            license_number="ABC12345",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        car.drivers.set((driver, ))
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "Test"
        password = "Testpasswd"
        license_number = "ABC12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
