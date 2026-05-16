from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver(self):
        driver = Driver.objects.create(
            username="test",
            password="test123",
            first_name="test first",
            last_name="test last",
            license_number="ABC12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url_driver(self):
        driver = Driver.objects.create(
            username="test",
            password="test123",
            first_name="test first",
            last_name="test last",
            license_number="ABC12345",
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        driver = Driver.objects.create(
            username="test",
            password="test123",
            first_name="test first",
            last_name="test last",
            license_number="ABC12345",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(str(car), f"{car.model}")
