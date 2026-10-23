from django.contrib.auth import get_user_model
from django.test import TestCase


class LoggedInTestCase(TestCase):
    """Creates a driver once per test class and logs them in before each
    test."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="admin.user",
            password="test12345",
            license_number="ADM12345",
        )

    def setUp(self):
        self.client.force_login(self.user)
