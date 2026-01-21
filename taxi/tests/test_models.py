from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_username = "testuser"
        cls.test_password = "testpassword123"
        cls.test_first_name = "John"
        cls.test_last_name = "Doe"
        cls.test_license_number = "ABC12345"

        cls.driver = get_user_model().objects.create_user(
            username=cls.test_username,
            password=cls.test_password,
            first_name=cls.test_first_name,
            last_name=cls.test_last_name,
            license_number=cls.test_license_number,
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")

    def test_manufacturer_str(self):
        # Використовуємо об'єкт, створений в setUpTestData
        self.assertEqual(str(self.manufacturer),
                         f"{self.manufacturer.name} "
                         f"{self.manufacturer.country}"
                         )

    def test_driver_str(self):
        # Використовуємо об'єкт, створений в setUpTestData
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_create_driver(self):
        temp_driver = get_user_model().objects.create_user(
            username="another_user",
            password="anotherpassword",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ98765"
        )
        self.assertEqual(temp_driver.username, "another_user")
        self.assertEqual(
            temp_driver.license_number,
            "XYZ98765")
        self.assertTrue(temp_driver.check_password("anotherpassword"))
