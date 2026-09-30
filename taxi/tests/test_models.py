from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ManufacturerModelTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        self.assertEqual(
            str(manufacturer),
            "Rover UK"
        )

    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        self.assertEqual(manufacturer.name, "Rover")
        self.assertEqual(manufacturer.country, "UK")


class DriverModelTest(TestCase):

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="admin123",
            password="password123",
            first_name="Admin",
            last_name="AdminLast",
            license_number="ABC123"
        )

        self.assertEqual(
            str(driver),
            "admin123 (Admin AdminLast)"
        )

    def test_create_driver(self):
        driver = Driver.objects.create_user(
            username="admin123",
            password="password123",
            license_number="ABC123"
        )

        self.assertEqual(driver.username, "admin123")
        self.assertEqual(driver.license_number, "ABC123")


class CarModelTest(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        car = Car.objects.create(
            model="Streetwise",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), "Streetwise")

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        car = Car.objects.create(
            model="Streetwise",
            manufacturer=manufacturer
        )

        self.assertEqual(car.model, "Streetwise")
        self.assertEqual(car.manufacturer, manufacturer)
