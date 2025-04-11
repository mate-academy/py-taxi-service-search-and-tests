from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


# Create your test here.
class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="Jamaica")
        f_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), f_str)

    def test_driver_str_and_license(self):
        driver = get_user_model().objects.create(
            username="testusername",
            password="pass",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="test_license_number",
        )
        f_str = f"{driver.username} ({driver.first_name} {driver.last_name})"
        self.assertEqual(
            str(driver),
            f_str)
        self.assertEqual(driver.license_number, "test_license_number")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test manufacturer")
        # driver = Driver.objects.create(username="test driver")
        car = Car.objects.create(model="test model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
