from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license"
        )

    def test_driver_license_number_listed(self):
        res = self.client.get(
            reverse("taxi:driver-list")
        )
        self.assertContains(res, self.driver.license_number)
