from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_driver_model_str(self):
        driver = get_user_model().objects.create_user(
            username="parker1",
            password="spider123456",
            first_name="Peter",
            last_name="Parker"
        )
        self.assertEqual(str(driver), "parker1 (Peter Parker)")

    def test_driver_license(self):
        driver = get_user_model().objects.create_user(
            username="parker1",
            password="spider123456",
            license_number="ABC12345"
        )
        self.assertEqual(driver.username, "parker1")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password("spider123456"))

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Honda Japan")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        car = Car.objects.create(
            model="RX7",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "RX7")
