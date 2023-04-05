from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen", country="Germany"
        )
        self.assertEqual(str(manufacturer), "Volkswagen Germany")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen", country="Germany"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_driver_license(self):
        username = "test"
        password = "test12345"
        license_number = "AOU12345"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
