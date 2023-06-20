from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        expected = "Audi Germany"

        self.assertEqual(str(manufacturer), expected)


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        car = Car.objects.create(
            model="A4",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="alice",
            password="test12345",
            first_name="Alice",
            last_name="Smith",
            license_number="ABC12345",
        )

    def test_driver_first_name_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("first_name").verbose_name
        expected = "first name"

        self.assertEqual(field_label, expected)

    def test_driver_last_name_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("last_name").verbose_name
        expected = "last name"

        self.assertEqual(field_label, expected)

    def test_driver_license_number_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name
        expected = "license number"

        self.assertEqual(field_label, expected)

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        expected = "alice (Alice Smith)"

        self.assertEqual(str(driver), expected)

    def test_driver_license_number(self):
        driver = get_user_model().objects.get(id=1)
        expected = "ABC12345"

        self.assertEqual(driver.license_number, expected)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        expected = "/drivers/1/"

        self.assertEqual(driver.get_absolute_url(), expected)
