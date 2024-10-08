from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelsTests(TestCase):
    """Tests for string representations of the models."""

    def test_driver_str(self):
        """Test the string representation of the Driver model."""
        driver = Driver.objects.create(
            username="test",
            first_name="first test",
            last_name="last test",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        """Test the string representation of the Car model."""
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Japan"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        """Test the string representation of the Manufacturer model."""
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )
