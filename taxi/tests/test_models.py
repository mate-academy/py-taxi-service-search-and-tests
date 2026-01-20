from django.test import TestCase, Client

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Japan",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name}"
            f" {manufacturer.country}",
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Driver 1",
            first_name="Driver 1",
            last_name="Driver 1",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username}"
            f" ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Japan"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        driver = Driver.objects.create(
            username="Driver 1",
            license_number="AAA12345",
        )
        self.assertEqual(driver.username, "Driver 1")
        self.assertEqual(driver.license_number, "AAA12345")
