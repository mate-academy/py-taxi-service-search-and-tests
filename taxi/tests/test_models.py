from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTests(TestCase):
    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "SDG12363"
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="SDG12363",
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
