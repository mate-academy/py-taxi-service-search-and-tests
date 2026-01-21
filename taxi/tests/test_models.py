from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        obj = Manufacturer.objects.create(
            name="testName",
            country="testCountry",
        )
        self.assertEqual(f"{obj.name} {obj.country}", str(obj))

    def test_create_user_and_str_method_check(self):
        user = get_user_model()
        obj = user.objects.create_user(
            username="test",
            password="test123",
            license_number="TES34238",
            first_name="Test",
            last_name="TestLast",
        )
        self.assertEqual(obj.username, "test")
        self.assertTrue(obj.check_password("test123"))
        self.assertEqual(obj.license_number, "TES34238")
        self.assertEqual(
            f"{obj.username} ({obj.first_name} {obj.last_name})",
            str(obj)
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        obj_car = Car.objects.create(
            model="Honda",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(obj_car), "Honda")
