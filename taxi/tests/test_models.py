from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver
from taxi.forms import validate_license_number


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testName", country="testCountry"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="testusername",
            first_name="testfirst",
            last_name="testlast"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testName", country="testCountry"
        )
        car = Car.objects.create(model="testModel", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")
