from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mitsubishi", country="Japan"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            license_number="AAA00000",
            first_name="test_firs",
            last_name="test_las  t",
            password="test123",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            license_number="AAA00000",
            first_name="test_firs",
            last_name="test_last",
            password="test123",
        )
        manufacturer = Manufacturer.objects.create(
            name="Mitsubishi", country="Japan"
        )
        car = Car.objects.create(
            model="Lancer",
            manufacturer=manufacturer,
        )
        car.drivers.set(
            [
                driver,
            ]
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self) -> None:
        username = "test"
        license_number = "AAA00000"
        password = "test123"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
