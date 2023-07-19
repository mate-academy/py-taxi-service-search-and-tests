from django.contrib.auth import get_user_model
from django.test import TestCase


class TestModels(TestCase):
    def test_create_driver_with_license_number(self):
        username = "vasyl"
        password = "password1234"
        license_number = "ALC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEquals(driver.license_number, license_number)
