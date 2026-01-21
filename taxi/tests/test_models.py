from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def test_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_with_license_number(self) -> None:
        username = "test"
        password = "test123"
        license_number = "test_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url(self) -> None:
        driver = get_user_model().objects.create_user(
            username="Test",
            password="Password123"
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    def test_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
