from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mercedes-cls",
            country="Germany"
        )
        expected = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected)

    def test_driver_str(self):
        driver = Driver.objects.create(
            license_number="DMG98456",
            username="johnny",
            first_name="John",
            last_name="Doe",
        )
        expected = f"{driver.username} ({driver.first_name} {driver.last_name})"
        self.assertEqual(str(driver), expected)

    def test_car_str(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer,
        )
        expected = car.model
        self.assertEqual(str(car), expected)
