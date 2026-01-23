from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTest(TestCase):

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        first_name = "test_first"
        last_name = "test_last"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
