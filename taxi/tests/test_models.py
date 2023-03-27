from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_str_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country_test"
        )
        self.assertEqual(str(manufacturer), "test country_test")


class DriverTest(TestCase):
    def test_str_driver(self):
        username = "test_driver"
        driver = get_user_model().objects.create(
            username=username,
            password="1234asdf",
            license_number="LLL23456"
        )

        self.assertEqual(str(driver), username)


class CarTest(TestCase):
    def test_str_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country_test"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
