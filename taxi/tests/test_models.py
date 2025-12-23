from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )

        driver = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword123@?",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="ABC12345"
        )

        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )

        car.drivers.add(driver)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.id}/"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.username, "TestUsername")
        self.assertTrue(driver.check_password("TestPassword123@?"))
        self.assertEqual(driver.first_name, "TestFirstName")
        self.assertEqual(driver.last_name, "TestLastName")
        self.assertEqual(driver.license_number, "ABC12345")

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(
            str(car),
            car.model
        )
