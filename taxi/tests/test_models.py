from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test",
            password="test_pass123",
            first_name="test first",
            last_name="test last",
            license_number="TES12345",
        )

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)

    def test_create_user_with_license_number(self):
        username = "test"
        password = "test_pass123"
        first_name = "test first"
        last_name = "test last"
        license_number = "TES12345"

        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
