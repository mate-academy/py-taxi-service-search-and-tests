from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Toyota")
        self.assertEqual(self.manufacturer.country, "Japan")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer)

    def test_car_creation(self):
        self.assertEqual(self.car.model, "Corolla")
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")


class DriverModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.driver = Driver.objects.create(
            username="driveruser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe"
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username,
                         "driveruser")
        self.assertEqual(self.driver.license_number,
                         "ABC12345")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "driveruser (John Doe)")

    def test_driver_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(),
                         f"/drivers/{self.driver.pk}/")
