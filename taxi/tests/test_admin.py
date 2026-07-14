from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test1234"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )

