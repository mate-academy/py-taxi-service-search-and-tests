from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3"
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test2",
            license_number="ABC12345"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)
