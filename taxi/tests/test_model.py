from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )

    def test_str(self):
        self.assertEqual(str(self.driver), "john_doe (John Doe)")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver1 = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        self.driver2 = Driver.objects.create(
            username="alex_smith",
            first_name="Alex",
            last_name="Smith",
            license_number="XYZ789"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver1, self.driver2])

    def test_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_manufacturer_relation(self):
        self.assertEqual(str(self.car.manufacturer), "Toyota Japan")

    def test_drivers_relation(self):
        drivers_usernames = list(
            self.car.drivers.values_list(
                "username", flat=True
            )
        )
        self.assertIn("john_doe", drivers_usernames)
        self.assertIn("alex_smith", drivers_usernames)
