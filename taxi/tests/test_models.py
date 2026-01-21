from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test_name", country="Test_country"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="Test_driver",
            first_name="Some",
            last_name="Driver",
            password="driver-password",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test_name", country="Test_country"
        )

        car = Car.objects.create(
            model="Test-model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self) -> None:
        username = "Test_driver"
        license_number = "AAA11111"
        password = "driver-password"
        driver = get_user_model().objects.create_user(
            username=username, license_number=license_number, password=password
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
