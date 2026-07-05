from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="Test Driver",
            password="Test Password",
            first_name="Test First",
            last_name="Test Last",
            license_number="TES12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_with_license_number(self):
        username = "Test Driver"
        password = "Test Password"
        license_number = "TES12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
