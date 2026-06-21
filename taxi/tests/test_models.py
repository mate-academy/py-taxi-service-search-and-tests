from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestManufacturer(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Manufacturer",
            country="US",
        )

    def setUp(self):
        self.manufacturer = Manufacturer.objects.get(name="Manufacturer")

    def test_name_label(self):
        field_label = self.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        field_label = self.manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_unique(self):
        self.assertRaises(
            IntegrityError,
            Manufacturer.objects.create,
            name="Manufacturer"
        )

    def test_str(self):
        expected_str = f"{self.manufacturer.name} {self.manufacturer.country}"
        self.assertEqual(str(self.manufacturer), expected_str)


class TestDriver(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test_user",
            license_number="ABC12345",
            password="qwerty",
        )

    def setUp(self):
        self.driver = Driver.objects.get(username="test_user")

    def test_license_number_label(self):
        field_label = self.driver._meta.get_field("license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_license_number_unique(self):
        self.assertRaises(
            IntegrityError,
            Driver.objects.create_user,
            username="test_user2",
            license_number="ABC12345",
            password="qwerty2",
        )

    def test_str(self):
        expected_str = (
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_str)

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")


class TestCar(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="US",
        )
        drivers = []
        for i in range(3):
            drivers.append(Driver.objects.create_user(
                username=f"test_user{i}",
                license_number=f"ABC1111{i}",
                password="qwerty",
            ))
        car = Car.objects.create(
            model="BMW M5",
            manufacturer=manufacturer,
        )
        car.drivers.set(drivers)

    def setUp(self):
        self.car = Car.objects.get(id=1)

    def test_model_label(self):
        field_label = self.car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_manufacturer_label(self):
        field_label = self.car._meta.get_field("manufacturer").verbose_name
        self.assertEqual(field_label, "manufacturer")

    def test_drivers_label(self):
        field_label = self.car._meta.get_field("drivers").verbose_name
        self.assertEqual(field_label, "drivers")

    def test_str(self):
        expected_str = self.car.model
        self.assertEqual(str(self.car), expected_str)
