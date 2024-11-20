from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            password="test_password123",
            license_number="ASD12345",
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})",
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )
        car.drivers.add(self.driver)
        self.assertEqual(str(car), car.model)

    def test_driver_password_saved_correctly(self):

        self.assertEqual(
            self.driver.check_password("test_password123"),
            True,
        )
