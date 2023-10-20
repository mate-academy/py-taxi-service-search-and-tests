from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Mitsubishi Motors", country="Japan"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.first()
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Mitsubishi Motors", country="Japan"
        )
        Car.objects.create(
            model="Mitsubishi Outlander",
            manufacturer=manufacturer
        )

    def test_car_str(self):
        car = Car.objects.first()
        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            "username": "test.user",
            "password": "test2068",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ASD12345",
        }

        get_user_model().objects.create_user(**self.user_data)

    def test_car_str(self):
        driver = get_user_model().objects.first()
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.first()
        self.assertEqual(
            driver.username, self.user_data["username"]
        )
        self.assertEqual(
            driver.first_name, self.user_data["first_name"]
        )
        self.assertEqual(
            driver.last_name, self.user_data["last_name"]
        )
        self.assertEqual(
            driver.license_number, self.user_data["license_number"]
        )
        self.assertTrue(
            driver.check_password(self.user_data["password"])
        )
