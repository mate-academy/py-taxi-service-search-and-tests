from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="testers_land"
        )
        self.assertEqual(
            str(manufacturer),
            "test testers_land"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="first",
            last_name="last",
        )

        self.assertEqual(
            str(driver),
            "test (first last)"
        )

    def test_create_driver_with_license(self):
        driver = Driver.objects.create(
            username="test",
            password="test123",
            first_name="first",
            last_name="last",
            license_number="QWE45678"
        )
        self.assertEqual(driver.license_number, "QWE45678")

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123"
        )

        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.id})

        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="uncle_Bob",
            country="Bob_lands"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "test_model")
