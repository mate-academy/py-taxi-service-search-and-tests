from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class TestDriverModel(TestCase):
    def test_model(self):
        driver = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.assertEqual(str(driver), "john_doe (John Doe)")


class TestCarModel(TestCase):
    def test_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "Camry")
        self.assertEqual(car.manufacturer, manufacturer)


class TestManufacturerModel(TestCase):
    def test_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.assertEqual(
            str(manufacturer),
            "Toyota Japan",
        )
