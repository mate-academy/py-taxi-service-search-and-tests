from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def setUp(self) -> None:

        self.driver = Driver.objects.create_user(
            username="Test",
            license_number="ABV12345",
            first_name="Test name",
            last_name="Test surname"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="1 name",
            country="country"
        )
        self.manufacture_2 = Manufacturer.objects.create(
            name="2 Test manufacturer name",
            country="Test manufacturer country"
        )

        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test"
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_fields_correct(self):
        self.assertEqual(
            self.manufacturer.name,
            "1 name"
        )
        self.assertEqual(
            self.manufacturer.country,
            "country"
        )

    def test_str_method_for_manufacturer(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_manufacturer_ordering_correct(self):
        self.assertEqual(
            [
                self.manufacturer,
                self.manufacture_2,
            ],
            list(Manufacturer.objects.all())
        )

    def test_str_method_for_car(self):
        self.assertEqual(
            str(self.car),
            self.car.model
        )

    def test_car_fields_correct(self):
        self.assertEqual(self.car.model, "Test")
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, self.car.drivers.all())

    def test_driver_license_number_correct(self):
        self.assertEqual(self.driver.license_number, "ABV12345")

    def test_str_method_for_driver(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
