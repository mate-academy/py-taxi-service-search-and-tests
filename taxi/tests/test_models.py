from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="C test",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(name="B test")
        self.manufacturer3 = Manufacturer.objects.create(
            name="A test",
            country="USA"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="password111",
            license_number="AAA12345",
            first_name="One",
            last_name="FirstDriver",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="password222",
            license_number="BBB12345",
            first_name="Two",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer1,
        )
        self.car.drivers.add(self.driver1, self.driver2)

    def test_manufacturer_ordering_by_name(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "A test")
        self.assertEqual(manufacturers[1].name, "B test")
        self.assertEqual(manufacturers[2].name, "C test")

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer1),
            f"{self.manufacturer1.name} {self.manufacturer1.country}"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_license_number(self):
        self.assertEqual(self.driver1.license_number, "AAA12345")

    def test_driver_verbose_name_plural(self):
        self.assertEqual(str(Driver._meta.verbose_name_plural), "drivers")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver2),
            f"{self.driver2.username} "
            f"({self.driver2.first_name} {self.driver2.last_name})"
        )
