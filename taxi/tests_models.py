from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

User = get_user_model()


class ManufacturerModelTest(TestCase):
    def test_str_returns_name_and_country(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")


class DriverModelTest(TestCase):
    def test_str_returns_username_and_full_name(self):
        driver = User.objects.create(
            username="driver1",
            password="test1234",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        self.assertEqual(str(driver), "driver1 (John Doe)")


class CarModelTest(TestCase):
    def test_str_returns_model_name(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(model="M5", manufacturer=manufacturer)
        self.assertEqual(str(car), "M5")
