from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="testusername",
            password="test54321",
            first_name="test firstname",
            last_name="test lastname",
            license_number="TES12345",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "testusername"
        password = "test54321"
        license_number = "TES12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_get_absolut_url(self):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="TestPassword",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})

        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), "test model")
