from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_superuser = get_user_model().objects.create_superuser(
            username="AdminUser",
            password="12121212@A",
            first_name="Admin",
            last_name="User",
            license_number="ABC12345"
        )
        self.client.force_login(self.admin_superuser)
        self.ordinary_user = get_user_model().objects.create_superuser(
            username="OrdinaryUser",
            password="12121212@A",
            first_name="Ordinary",
            last_name="User",
            license_number="ABC12346"
        )

    def test_drive_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.ordinary_user.license_number)

    def test_drive_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.ordinary_user.id])
        response = self.client.get(url)
        self.assertContains(response, self.ordinary_user.license_number)
