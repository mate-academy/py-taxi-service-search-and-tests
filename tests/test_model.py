from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestManufacturerModel(TestCase):
    def test_string_representation(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.assertEqual(str(manufacturer), "Ford USA")


class TestCarModel(TestCase):
    def test_string_representation(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(model="Focus", manufacturer=manufacturer)
        self.assertEqual(str(car), "Focus")


class TestDriverModel(TestCase):
    def test_string_representation(self):
        driver = get_user_model().objects.create(
            username="john", first_name="John", last_name="Smith"
        )
        self.assertEqual(str(driver), "john (John Smith)")
