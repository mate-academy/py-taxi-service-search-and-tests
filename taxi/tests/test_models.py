from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test M",
            country="Test C",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test user",
            license_number="TES34591",
            password="test123password",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test M",
            country="Test C",
        )
        drivers = Driver.objects.create(
            username="test user",
        )
        car = Car.objects.create(
            model="model",
            manufacturer=manufacturer,
        )
        car.drivers.set([drivers])
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test user"
        license_number = "TES34591"
        password = "password123test"
        driver = Driver.objects.create_user(
            username=username,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
