from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class StringRepresentTest(TestCase):
    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country Test"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver(self):
        driver = Driver.objects.create_user(
            username="test123",
            password="test321",
            license_number="ABC12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country Test"
        )

        car = Car.objects.create(
            model="RS6",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)
