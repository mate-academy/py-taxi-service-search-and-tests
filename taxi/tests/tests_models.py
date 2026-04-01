from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


# Create your tests here.
class ManufacturerTestModel(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="DE"
        )

    def test_str(self):
        self.assertEqual(str(self.manufacturer), "BMW DE")


class DriverTestModel(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="jdoe",
            password="test-pass-123",
            license_number="LIC-001",
            first_name="John",
            last_name="Doe",
        )

    def test_str(self):
        self.assertEqual(str(self.driver), "jdoe (John Doe)")


class CarTestModel(TestCase):
    def setUp(self):
        from taxi.models import Manufacturer, Car

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

    def test_str(self):
        self.assertEqual(str(self.car), "Corolla")
