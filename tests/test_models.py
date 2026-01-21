# tests/test_models.py

from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer, Driver


class TestDriverModel(TestCase):  # Correct class name
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )

    def test_driver_str_method(self):
        self.assertEqual(str(self.driver),
                         "testdriver (John Doe)")

    def test_license_number_unique(self):
        with self.assertRaises(Exception):
            Driver.objects.create_user(
                username="anotherdriver",
                password="password123",
                first_name="Jane",
                last_name="Doe",
                license_number="ABC12345",
            )

    def test_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


class TestCarModel(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Tesla")
        self.driver1 = Driver.objects.create_user(
            username="admin.alex",
            password="password123",
            first_name="Alex",
            last_name="Smith",
            license_number="ABC123",
        )
        self.driver2 = Driver.objects.create_user(
            username="vova",
            password="password123",
            first_name="Vova",
            last_name="Doe",
            license_number="DEF456",
        )

        self.car = Car.objects.create(
            model="Tesla_Sport", manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver1, self.driver2])

    def test_car_str_method(self):
        self.assertEqual(str(self.car), "Tesla_Sport")


class TestManufacturerModel(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="KIA")

    def test_manufacturer_str_method(self):
        self.assertEqual("KIA", self.manufacturer.name)
