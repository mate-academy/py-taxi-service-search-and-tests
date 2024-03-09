from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="12345678"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="TesCountry"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="TestUser",
            first_name="Admin",
            last_name="Last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="TesCountry"
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="Toyota"
        )

        self.assertEqual(str(car), car.model)

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="TestUser",
            first_name="Admin",
            last_name="Last"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.id}/"
        )

    def test_driver_creation(self):
        driver = get_user_model().objects.get(username="test_user")
        self.assertEqual(driver.license_number, "12345678")
