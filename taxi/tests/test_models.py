from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Toyota")
        self.assertEqual(self.manufacturer.country, "Japan")
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "BMW")
        self.assertEqual(manufacturers[2].name, "Toyota")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "driver1")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "ABC123")
        self.assertEqual(str(self.driver), "driver1 (John Doe)")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="testpass456",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ789"
        )

    def test_car_creation(self):
        self.assertEqual(self.car.model, "Corolla")
        self.assertEqual(self.car.manufacturer.name, "Toyota")
        self.assertEqual(str(self.car), "Corolla")

    def test_car_drivers(self):
        self.car.drivers.add(self.driver1, self.driver2)
        self.assertIn(self.driver1, self.car.drivers.all())
        self.assertIn(self.driver2, self.car.drivers.all())
        self.assertEqual(self.car.drivers.count(), 2)
