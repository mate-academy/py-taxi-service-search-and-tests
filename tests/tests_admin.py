from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class TestsForAdminPanel(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="test1",
            password="admin-123",
        )
        self.client.force_login(self.user_admin)
        self.user_driver = get_user_model().objects.create_user(
            username="test2", password="admin-123", license_number="AAA12345"
        )

    def test_license_number(self):
        url = "http://localhost/admin/taxi/driver/"
        res = self.client.get(url)
        self.assertContains(res, self.user_driver.license_number)
