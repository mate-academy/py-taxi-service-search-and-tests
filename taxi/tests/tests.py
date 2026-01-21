from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Cadillac",
            country="USA",
        )
        self.assertEqual(str(manufacturer), "Cadillac USA")


class DriverTest(TestCase):

    def test_create_licence_number(self):
        username = "Testusername"
        first_name = "Testfisstname"
        last_name = "Testlastname"
        license_number = "ABC12345"
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


class CarTestModel(TestCase):
    def test_create_car_model(self):
        manufacturer = Manufacturer.objects.create(
            country="Germany",
            name="Volkswagen"
        )
        car = Car.objects.create(
            model="CC",
            manufacturer=manufacturer)
        self.assertEqual(str(car), "CC")
        self.assertEqual(car.manufacturer, manufacturer)
