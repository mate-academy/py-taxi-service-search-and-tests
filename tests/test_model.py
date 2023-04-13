from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="john_smith",
            first_name="John",
            last_name="Smith",
            password="admin.admin",
            license_number="ADC43567"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car = Car.objects.create(
            model="Ford",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name}"
            f" {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self) -> None:
        url = self.driver.get_absolute_url()

        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(url, expected_url)

    def test_driver_license_number(self) -> None:
        self.assertEqual(self.driver.license_number, "ADC43567")
        self.assertTrue(self.driver.check_password("admin.admin"))
