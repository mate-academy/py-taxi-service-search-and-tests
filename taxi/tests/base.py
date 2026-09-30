from django.contrib.auth import get_user_model
from django.test import TestCase


class LoggedInTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
