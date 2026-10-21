from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            email="test@test.com",
            password="1234test",
            license_number="1234test",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
