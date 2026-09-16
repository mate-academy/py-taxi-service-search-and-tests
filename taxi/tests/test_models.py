from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer-test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer-test")
        driver = Driver.objects.create(
            username="Username-test",
            license_number="ABC12345",
        )
        car = Car.objects.create(
            model="Model-test",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = Driver.objects.create(
            license_number="ABC12345",
            username="Username-test",
            first_name="FirstName-test",
            last_name="LastName-test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver(self):
        username = "Username-test"
        license_number = "ABC12345"
        first_name = "FirstName-test"
        last_name = "LastName-test"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
