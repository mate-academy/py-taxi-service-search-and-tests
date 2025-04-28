from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ManufacturerModelTest(TestCase):
    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")
        self.assertEqual(manufacturer.name, "Toyota")
        self.assertEqual(manufacturer.country, "Japan")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            first_name="Test",
            last_name="Driver",
            license_number="ABC12345",
        )

    def test_create_driver(self):
        self.assertEqual(str(self.driver), "testdriver (Test Driver)")
        self.assertEqual(self.driver.license_number, "ABC12345")

    def test_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(url, expected_url)


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.driver = Driver.objects.create_user(
            username="bmwdriver",
            password="password123",
            first_name="BMW",
            last_name="Driver",
            license_number="BMW12345",
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_create_car(self):
        self.assertEqual(str(self.car), "X5")
        self.assertEqual(self.car.manufacturer.name, "BMW")

    def test_car_drivers(self):
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())
