from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test_user",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "test_user (John Doe)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        car = Car.objects.create(model="Model S", manufacturer=manufacturer)
        self.assertEqual(str(car), "Model S")
