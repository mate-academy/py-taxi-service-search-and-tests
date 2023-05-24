from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class TestForModels(TestCase):
    def test_manufacturer_str(self):
        example = Manufacturer.objects.create(
            country="Ukraine",
            name="Auto"
        )
        self.assertEquals(str(example), "Auto Ukraine")

    def test_car_str(self):
        example = Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.create(
                name="test",
                country="test"),
        )
        self.assertEquals(str(example), "test")

    def test_driver_str(self):
        example = Driver.objects.create_user(
            username="ts",
            first_name="Taras",
            last_name="Savchyn",
            password="admin-123"
        )
        self.assertEquals(str(example), "ts (Taras Savchyn)")

    def test_lisence_number(self):
        example = Driver.objects.create_user(
            username="ts",
            first_name="Taras",
            last_name="Savchyn",
            password="admin-123",
            license_number="AAA12345",
        )
        self.assertEquals(example.username, "ts")
        self.assertTrue(example.check_password("admin-123"))
        self.assertEquals(example.license_number, "AAA12345")
