from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Carl", country="USA")
        self.assertEqual(str(manufacturer),
                         manufacturer.name + " " + manufacturer.country)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test_user",
            password="Test_pass",
            first_name="Test_first",
            last_name="Test_last",
        )

        self.assertEqual(str(driver), f"{driver.username}"
                                      f" ({driver.first_name}"
                                      f" {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Carl", country="USA")
        car = Car.objects.create(
            model="TEST",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_license_number_create(self):
        password = "Testpass123"
        driver = get_user_model().objects.create_user(
            username="Test_name",
            password=password,
            license_number="Test12345",
        )

        self.assertEqual(driver.username, "Test_name")
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, "Test12345")
