from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


User = get_user_model()


class ManufacturerModelTest(TestCase):
    def test_str_returns_name_and_country(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.assertEqual(str(manufacturer), "Ford USA")


class DriverModelTest(TestCase):
    def test_str_returns_username_and_full_name(self):
        driver = User.objects.create(
            username="driver1",
            password="test1234",
            first_name="Bob",
            last_name="Glass",
            license_number="ABC123"
        )
        self.assertEqual(str(driver), "driver1 (Bob Glass)")


class CarModelTest(TestCase):
    def test_str_returns_model_name(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        car = Car.objects.create(model="Q5", manufacturer=manufacturer)
        self.assertEqual(str(car), "Q5")
