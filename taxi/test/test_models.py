from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            first_name="John",
            last_name="Doe",
            license_number="AAA12345"
        )
        self.assertEqual(str(driver), "testdriver (John Doe)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")
