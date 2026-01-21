from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        car = Car.objects.create(
            model="Test_model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test_username",
            first_name="Test_first_name",
            last_name="Test_last_name"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="Test_username",
            first_name="Test_first_name",
            last_name="Test_last_name"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")

    def test_create_driver_with_license_number(self):
        username = "Test_username"
        password = "TestPassword123"
        license_number = "Test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
