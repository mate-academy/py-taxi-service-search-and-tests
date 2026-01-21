from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Random"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Test Driver",
            first_name="Test First",
            last_name="Test Last",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name}"
                         f" {driver.last_name})")

    def test_car_str(self):
        Driver.objects.create(
            username="Test Driver",
            first_name="Test First",
            last_name="Test Last",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model",
        )
        self.assertEqual(str(car), f"{car.model}")
