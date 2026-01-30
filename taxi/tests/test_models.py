from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="testcountry"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test12345",
            first_name="testdriverfirst",
            last_name="testdriverlast",
            license_number="AXE54321"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="testcountry"
        )
        car = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test12345",
            license_number="AXE54321",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
