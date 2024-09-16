from django.contrib.auth import get_user_model
from django.test import TestCase


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
            email="test@example.com",
            license_number="ABC123"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "testuser (John Doe)")

    def test_driver_get_absolute_url(self):
        expected_url = "/drivers/" + str(self.driver.pk) + "/"
        self.assertEqual(self.driver.get_absolute_url(), expected_url)
