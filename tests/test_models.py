from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_model_creation(self):
        username = "test"
        first_name = "test first name"
        last_name = "test last name"
        license_number = "TES84723"
        driver = get_user_model().objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)

    def test_create_car_model(self):
        manufacturer = Manufacturer.objects.create(
            country="Italy",
            name="Ferrari"
        )
        car = Car.objects.create(
            model="250 GTO",
            manufacturer=manufacturer)
        self.assertEqual(str(car), "250 GTO")
        self.assertEqual(car.manufacturer, manufacturer)
