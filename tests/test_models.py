from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="driver1",
            password="password123",
            first_name="Test_first",
            last_name="Test_last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "user1"
        password = "password123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
