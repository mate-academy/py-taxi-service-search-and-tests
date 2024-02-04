from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):
    def test_model_str_method(self):
        obj = Manufacturer.objects.create(
            name="Car manufacturer",
            country="USA")
        self.assertEqual(str(obj), f"{obj.name} {obj.country}")


class DriverTest(TestCase):
    def test_user_model_created_with_license_number(self):
        obj = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456", license_number="124"
        )
        self.assertEqual(obj.username, "user-user")

    def test_model_str_method(self):
        obj = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456", license_number="124"
        )
        self.assertEqual(
            str(obj),
            f"{obj.username} ({obj.first_name} {obj.last_name})"
        )


class CarTest(TestCase):
    def test_model_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Car manufacturer", country="USA"
        )
        obj = Car.objects.create(model="Car model", manufacturer=manufacturer)
        self.assertEqual(str(obj), obj.model)
