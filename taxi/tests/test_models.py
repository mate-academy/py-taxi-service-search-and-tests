from django.test import TestCase
from taxi.models import (
    Manufacturer,
    Driver,
    Car
)


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="dimka",
            password="12345dimka",
            first_name="dmytro",
            last_name="samoylenko"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )
        car = Car.objects.create(
            model="8C",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            f"{car.manufacturer.name} {car.model}"
        )

    def test_create_driver_with_license_number(self):
        username = "dimka"
        password = "12345dimka"
        license_number = "ABC12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
