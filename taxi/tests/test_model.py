from django.test import TestCase
from taxi.models import Manufacturer
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacture = Manufacturer.objects.create(name="test",
                                                  country="USA")
        self.assertEqual(str(manufacture),
                         f"{manufacture.name} {manufacture.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="123",
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_additional_license_number_str(self):
        username = "test"
        license_number = "123"
        password = "test123test"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
