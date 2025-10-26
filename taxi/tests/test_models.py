from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="TestCountry"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="TestCountry"
        )

        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_driving_license(self):
        username = "test"
        password = "test123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        expected_url = f"/drivers/{driver.pk}/"
        self.assertEqual(driver.get_absolute_url(), expected_url)
