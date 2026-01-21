from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class TestModels(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="testdriver",
            first_name="Test",
            last_name="Driver",
            license_number="ABC12345",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test",
        )

    def test_driver_str(self):
        driver = self.driver

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

        self.assertEqual(str(car), car.model)
