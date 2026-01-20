from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Toyota")
        self.assertEqual(self.manufacturer.country, "Japan")
        self.assertIsInstance(self.manufacturer, Manufacturer)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="driver1",
            first_name="test_first",
            last_name="test_last",
            password="password123",
            license_number="ABC12345",
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "driver1")
        self.assertEqual(self.driver.first_name, "test_first")
        self.assertEqual(self.driver.last_name, "test_last")
        self.assertEqual(self.driver.password, "password123")
        self.assertEqual(self.driver.license_number, "ABC12345")
        self.assertIsInstance(self.driver, Driver)

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_car_creation(self):
        self.assertEqual(self.car.model, "Corolla")
        self.assertEqual(self.car.manufacturer.name, "Toyota")
        self.assertIsInstance(self.car, Car)

    def test_car_str(self):
        self.assertEqual(str(self.car), f"{self.car.model}")
