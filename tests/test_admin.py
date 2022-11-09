from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="driver123", license_number="ABC12345"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)
