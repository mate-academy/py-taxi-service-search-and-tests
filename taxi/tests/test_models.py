from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Model S",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_format_str(self):
        driver = Driver.objects.create(
            username="gangster288",
            password="testpassword",
            first_name="Antonio",
            last_name="Montana",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_format_str(self):
        car = Car.objects.create(
            model="Tesla",
            manufacturer=Manufacturer.objects.create(
                name="Model S",
                country="USA"
            ),
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "heisenberg"
        password = "1234test"
        license_number = "AAA00001"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
