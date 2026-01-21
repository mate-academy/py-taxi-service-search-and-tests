from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="test_fn",
            last_name="test_ln"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        license_number = "test_lnumber"

        driver = get_user_model().objects.create(
            username=username,
            license_number=license_number
        )

        self.assertEqual(username, driver.username)
        self.assertEqual(license_number, driver.license_number)

    def test_get_absolute_url(self):
        driver = Driver.objects.create(
            username="test_user",
            first_name="test_fn",
            last_name="test_ln",
            license_number="ABC12345"
        )

        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
