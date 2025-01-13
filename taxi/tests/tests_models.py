from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


# Create your tests here.


class ManufacturerModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )  # NOQA E501
        self.assertEqual(str(manufacturer), "Toyota Japan")


class DriverModelTest(TestCase):
    def test_str_method(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
            license_number="ABC123",
        )
        self.assertEqual(str(user), "testuser (John Doe)")


class CarModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )  # NOQA E501
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")
