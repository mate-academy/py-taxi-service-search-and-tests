from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Tesla")
        self.assertEqual(self.manufacturer.country, "USA")

    def test_unique_name_constraint(self):
        with self.assertRaises(Exception):
            Manufacturer.objects.create(name="Tesla", country="Canada")

    def test_str_method(self):
        self.assertEqual(str(self.manufacturer), "Tesla USA")

    def test_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "BMW")
        self.assertEqual(manufacturers[2].name, "Tesla")

    def test_name_max_length(self):
        manufacturer = Manufacturer(name="a" * 256, country="Germany")
        with self.assertRaises(ValidationError):
            manufacturer.full_clean()

    def test_country_max_length(self):
        manufacturer = Manufacturer(name="BMW", country="a" * 256)
        with self.assertRaises(ValidationError):
            manufacturer.full_clean()


class DriverModelTest(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpassword123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "driver1")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "ABC12345")

    def test_unique_license_number_constraint(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="driver2",
                password="testpassword456",
                first_name="Jane",
                last_name="Smith",
                license_number="ABC12345"
            )

    def test_str_method(self):
        self.assertEqual(str(self.driver), "driver1 (John Doe)")

    def test_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        self.assertEqual(url, expected_url)


class CarModelTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )

        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="testpassword123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="testpassword456",
            first_name="Jane",
            last_name="Smith",
            license_number="DEF67890"
        )

        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

        self.car.drivers.add(self.driver1, self.driver2)

    def test_car_creation(self):
        self.assertEqual(self.car.model, "Model S")
        self.assertEqual(self.car.manufacturer.name, "Tesla")

    def test_str_method(self):
        self.assertEqual(str(self.car), "Model S")

    def test_car_drivers(self):
        self.assertIn(self.driver1, self.car.drivers.all())
        self.assertIn(self.driver2, self.car.drivers.all())

    def test_manufacturer_relationship(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)
