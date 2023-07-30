from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="testpassword12345",
            first_name="Tester",
            last_name="Testenko",
            license_number="AIA12345"
        )

        self.assertEqual(str(driver), "test_username (Tester Testenko)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford Motor Co.",
            country="USA"
        )
        car = Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_licnse(self):
        username = "test123"
        password = "testpassword123"
        license_number = "TST12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
