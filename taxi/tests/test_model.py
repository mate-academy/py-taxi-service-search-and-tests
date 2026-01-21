from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    driver = {
        "username": "shel.don",
        "password": "<PASSWORD>",
        "first_name": "Sheldon",
        "last_name": "Cooper",
    }
    manufacturer = {
        "name": "Land Rover",
        "country": "United Kingdom",
    }

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(**self.manufacturer)
        self.assertEqual(str(manufacturer), "Land Rover United Kingdom")

    def test_driver(self):
        driver = Driver.objects.create_user(**self.driver)
        self.assertEqual(str(driver), "shel.don (Sheldon Cooper)")
        self.assertTrue(driver.check_password("<PASSWORD>"))

    def test_driver_license_number(self):
        driver = Driver.objects.create_user(**self.driver)
        driver.license_number = "ABC12345"
        self.assertEqual(driver.license_number, "ABC12345")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(**self.manufacturer)
        car = Car.objects.create(
            model="Range Rover Sport",
            manufacturer=manufacturer,

        )
        self.assertEqual(str(car), "Range Rover Sport")
