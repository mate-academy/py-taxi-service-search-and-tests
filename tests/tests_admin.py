from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.admin_user = get_user_model().objects.create_user(
            username="admin1",
            password="testadmin123",
            license_number="ABC12345",
        )

    def test_user_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.admin_user.license_number)

    def test_user_detail_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.admin_user.id])
        res = self.client.get(url)
        self.assertContains(res, self.admin_user.license_number)
