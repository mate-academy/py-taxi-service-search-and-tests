from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")


class DriverTest(TestCase):
    LICENSE_NUMBER = "ABC12345"

    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test",
            password="1qazcde3",
            license_number=self.LICENSE_NUMBER
        )

    def test_drivers_str(self):
        self.assertEqual(str(self.driver),
                         f"{self.driver.username} "
                         f"({self.driver.first_name} {self.driver.last_name})"
                         )

    def test_unique_license_number(self):
        with self.assertRaises(IntegrityError):
            Driver.objects.create_user(
                username="test2",
                password="1qazcde3",
                license_number=self.LICENSE_NUMBER
            )

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_verbose_name(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")

    def test_verbose_name_plural(self):
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")


class CarTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test",
            password="1qazcde3",
            license_number="ABC12345"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine"
        )
        car = Car.objects.create(model="Audi", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
