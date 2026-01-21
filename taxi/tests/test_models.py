from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ManufacturerModelTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class DriverModelTest(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            first_name="Narberal",
            last_name="Gamma",
            password="password123",
            license_number="ABC23456",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "testdriver (Narberal Gamma)")


class CarModelTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.driver = Driver.objects.create_user(
            username="cardriver",
            first_name="Narberal",
            last_name="Gamma",
            password="password123",
            license_number="CD987654",
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_str(self):
        self.assertEqual(str(self.car), "X5")

    def test_car_driver_relationship(self):
        self.assertIn(self.driver, self.car.drivers.all())
