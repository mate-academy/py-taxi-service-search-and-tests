from django.test import TestCase
from taxi.models import Car, Manufacturer, Driver

class ManufacturerModelTest(TestCase):
    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.assertEqual(manufacturer.name, "Toyota")
        self.assertEqual(manufacturer.country, "Japan")
        self.assertEqual(str(manufacturer), "Toyota Japan")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        self.car = Car.objects.create(model="X5", manufacturer=self.manufacturer)

    def test_create_car(self):
        self.assertEqual(self.car.model, "X5")
        self.assertEqual(self.car.manufacturer.name, "BMW")
        self.assertEqual(str(self.car), "X5")


class DriverModelTest(TestCase):
    def test_create_driver(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(driver.username, "testdriver")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertEqual(str(driver), "testdriver (John Doe)")
