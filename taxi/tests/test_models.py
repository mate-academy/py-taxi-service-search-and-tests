from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer_str = Manufacturer.objects.create(
            name="test",
            country="testcountry"
        )
        self.assertEqual(
            str(manufacturer_str),
            f"{manufacturer_str.name}"
            f" {manufacturer_str.country}"
        )

    def test_driver_str(self):
        driver_str = Driver.objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver_str),
            f"{driver_str.username} "
            f"({driver_str.first_name} "
            f"{driver_str.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ASD12345",
        )
        self.assertEqual(
            driver.username,
            "test"
        )
        self.assertEqual(
            driver.license_number,
            "ASD12345"
        )
        self.assertTrue(driver.check_password("test123"))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ASD12345",
        )
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": driver.pk}
        )
        self.assertEqual(
            driver.get_absolute_url(),
            expected_url
        )

    def test_car_str(self):
        car_str = Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.create(
                name="test",
                country="testcountry"
            )
        )
        self.assertEqual(str(car_str), car_str.model)
