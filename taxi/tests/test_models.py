from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test1",
            password="test123",
            first_name="first",
            last_name="last",
            license_number="ABC12345",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            (
                f"{self.driver.username} "
                f"({self.driver.first_name} {self.driver.last_name})"
            )
        )

    def test_driver_create_with_license_number(self):
        self.assertEqual(self.driver.username, "test1")
        self.assertTrue(self.driver.check_password("test123"))
        self.assertEqual(
            self.driver.license_number,
            "ABC12345"
        )

    def test_driver_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
