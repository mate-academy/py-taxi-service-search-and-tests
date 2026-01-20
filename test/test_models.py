from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth import get_user_model


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_manufacturer_ordering(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "Toyota")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
            license_number="12345ABC",
            password="testpass123"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "testuser (John Doe)")

    def test_driver_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/"
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            first_name="Jane",
            last_name="Doe",
            license_number="98765XYZ",
            password="testpass456"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_car_drivers(self):
        self.assertIn(self.driver, self.car.drivers.all())

    def test_car_manufacturer(self):
        self.assertEqual(self.car.manufacturer.name, "Toyota")
