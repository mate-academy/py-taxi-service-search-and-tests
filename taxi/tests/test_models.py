from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="USA",
        )

    def test_str(self):
        self.assertEqual(
            str(self.manufacturer), "Toyota USA"
        )

    def test_name_is_unique(self):
        with self.assertRaises(Exception):
            Manufacturer.objects.create(
                name="Toyota",  # така назва вже є
                country="USA"
            )

    def test_name_max_length(self):
        max_length = self.manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        max_length = self.manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "BMW")
        self.assertEqual(manufacturers[2].name, "Toyota")


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="john1337",
            password="123123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_str(self):
        self.assertEqual(str(self.driver), "john1337 (John Doe)")

    def test_license_number_max_length(self):
        max_length = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 8)

    def test_license_number_is_unique(self):
        with self.assertRaises(Exception):
            Driver.objects.create(license_number="ABC12345")


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.driver = get_user_model().objects.create_user(
            username="john1337",
            password="123123",
            license_number="ABC12345",
        )

        self.car = Car.objects.create(
            model="MX-5",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_str(self):
        self.assertEqual(str(self.car), "MX-5")

    def test_manufacturer(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_driver_in_car(self):
        self.assertIn(self.driver, self.car.drivers.all())

    def test_cascade_delete(self):
        self.manufacturer.delete()
        self.assertFalse(Car.objects.filter(model="MX-5").exists())

    def test_model_max_length(self):
        max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)
