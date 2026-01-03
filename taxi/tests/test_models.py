from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car

User = get_user_model()


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Toyota")
        self.assertEqual(self.manufacturer.country, "Japan")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_manufacturer_unique_name(self):
        with self.assertRaises(Exception):
            Manufacturer.objects.create(name="Toyota", country="USA")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = User.objects.create_user(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="ABC123456"
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "driver1")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "ABC123456")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "driver1 (John Doe)")

    def test_driver_unique_license_number(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="driver2",
                first_name="Jane",
                last_name="Smith",
                license_number="ABC123456"
            )

    def test_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertEqual(
            url, reverse(
                "taxi:driver-detail", kwargs={"pk": self.driver.pk}
            )
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.driver = User.objects.create_user(
            username="driver3",
            first_name="Alice",
            last_name="Cooper",
            license_number="XYZ987654"
        )
        self.car = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_creation(self):
        self.assertEqual(self.car.model, "Civic")
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_car_str(self):
        self.assertEqual(str(self.car), "Civic")

    def test_car_driver_relationship(self):
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())
