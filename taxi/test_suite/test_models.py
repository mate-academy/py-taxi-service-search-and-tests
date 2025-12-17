from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    def test_str_returns_name(self):
        manufacturer = Manufacturer.objects.create(name="BMW Germany")
        self.assertEqual(str(manufacturer).strip(), "BMW Germany")


class CarModelTest(TestCase):
    def test_str_returns_model(self):
        manufacturer = Manufacturer.objects.create(name="BMW Germany")
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car).strip(), "X5")


class DriverModelTest(TestCase):
    def test_str_contains_username(self):
        driver = Driver.objects.create(username="ivan",
                                       license_number="TES12345")
        self.assertIn(driver.username, str(driver))
