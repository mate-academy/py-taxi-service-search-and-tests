from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name")
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test_password123"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(
            driver.username,
            username
        )
        self.assertTrue(driver.check_password(password))
        self.assertEqual(
            driver.license_number,
            license_number
        )

    def test_get_absolute_url_for_driver(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123",
            license_number="test_license_number"
        )
        actual_url = driver.get_absolute_url()
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})

        self.assertEqual(actual_url, expected_url)
