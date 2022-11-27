from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="AAA",
            country="Ukraine"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test",
            last_name="Testson",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_licence(self):
        username = "test",
        license_number = "AAA00000"
        driver = get_user_model().objects.create_user(
            username=username,
            password="test12345",
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password("test12345"))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="AAA",
            country="Ukraine"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
