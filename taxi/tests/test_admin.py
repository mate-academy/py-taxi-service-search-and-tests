from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin", email="EMAIL", password="PASSWORD"
        )
        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(
            username="user", email="EMAIL", password="PASSWORD"
        )
