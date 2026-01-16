from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.assertEqual(str(manufacturer), "Tesla USA")


class DriverModelTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            "testdriver (John Doe)"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpass123",
            license_number="ABC12345"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.id}/"
        )

    def test_create_driver_with_license_number(self):
        username = "testdriver"
        password = "testpass123"
        license_number = "ABC12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Model 3",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car), "Model 3")
