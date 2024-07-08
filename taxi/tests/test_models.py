from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModelsStr(TestCase):
    def test_manufacture_str(self):
        obj = Manufacturer.objects.create(name="test", country="test123")
        self.assertEqual(str(obj), f"{obj.name} {obj.country}")

    def test_driver_str(self):
        obj = Driver.objects.create(
            username="test",
            password="pass",
            first_name="test1",
            last_name="test2",
            license_number="LLL12345",
        )
        self.assertEqual(
            str(obj),
            f"{obj.username} ({obj.first_name} {obj.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test123"
        )
        obj = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(obj), obj.model)
