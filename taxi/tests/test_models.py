from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="testuser",
            license_number="TST12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer(
            name="Test manufacturer",
            country="Test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_create_with_license_number(self) -> None:
        username, password, license_number = (
            "testuser", "test12345", "TST23232"
        )
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
