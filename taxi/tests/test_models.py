from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="USA"
        )

        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="user_name",
            first_name="John",
            last_name="Saron",
            license_number="test"
        )

        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="USA"
        )

        car = Car.objects.create(
            model="Tesla",
            manufacturer=manufacturer,
        )
        
        self.assertEqual(str(car), car.model)
