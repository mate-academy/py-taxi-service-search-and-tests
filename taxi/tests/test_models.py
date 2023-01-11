from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModuleTests(TestCase):

    def test_manufacturer_str(self):

        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test21234",
            first_name="test test",
            last_name="test test"
        )

        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        model = Car(
            model="test"
        )

        self.assertEqual(str(model), model.model)

    def test_create_driver_with_license_number(self):
        username = "Test"
        password = "test12345"
        license_number = "Test number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
