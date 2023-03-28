from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Round", country="Flatland")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer(name="Round", country="Flatland")
        car = Car(
            model="RX 977",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="Test",
            last_name="Testiloto"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license(self):
        driver = get_user_model().objects.create_user(
            username="mr.test",
            password="password_123",
            license_number="OMM98093"
        )
        self.assertTrue(driver.check_password("password_123"))
        self.assertEqual(driver.license_number, "OMM98093")
