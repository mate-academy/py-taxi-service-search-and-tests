from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

    def test_str_method(self):
        expected_output = "Test Manufacturer Test Country"
        self.assertEqual(str(self.manufacturer), expected_output)


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.driver = Driver.objects.create(first_name="John")
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_str_method(self):
        self.assertEqual(str(self.car), "Corolla")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(username="johndoe",
                                            first_name="John",
                                            last_name="Doe",
                                            license_number="ABC123")

    def test_str_method(self):
        self.assertEqual(str(self.driver), "johndoe (John Doe)")

    def test_license_number(self):
        self.assertEqual(self.driver.license_number, "ABC123")
