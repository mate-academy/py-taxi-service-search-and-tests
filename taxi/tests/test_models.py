from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class TestStringMethods(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.user = get_user_model().objects.create_user(
            license_number="AAA12345",
            username="admin",
            password="1a2T3e4u6v0",
            first_name="Test",
            last_name="Tester"
        )
        self.car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer),
                         f"{self.manufacturer.name} "
                         f"{self.manufacturer.country}")

    def test_driver_str(self):
        self.assertEqual(str(self.user),
                         f"{self.user.username} "
                         f"({self.user.first_name} "
                         f"{self.user.last_name})")

    def test_car_str(self):
        self.assertEqual(str(self.car),
                         self.car.model)

    def test_create_driver_with_license(self):
        self.assertEqual(self.user.license_number, "AAA12345")

    def test_user_verbose_name_singular(self):
        self.assertEqual(self.user._meta.verbose_name, "driver")

    def test_user_verbose_name_plural(self):
        self.assertEqual(self.user._meta.verbose_name_plural, "drivers")

    def test_if_manufacturers_ordered_by_name(self):
        Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )
        self.assertEqual(Manufacturer.objects.first().name, "Alfa Romeo")
