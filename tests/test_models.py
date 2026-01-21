from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})",
        )

    def test_get_driver_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            first_name="Test",
            last_name="User",
        )
        self.assertEquals(driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license_number(self):
        username = "test_user"
        password = "test12345"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        car = Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.create()
        )
        self.assertEqual(str(car), f"{car.model}")
