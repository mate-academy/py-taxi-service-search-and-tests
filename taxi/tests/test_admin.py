from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="sakhaline",
            password="54321gfdsa",
            license_number="AAA11111"
        )
        self.client.force_login(self.admin_user)

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.admin_user.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.admin_user.id])
        response = self.client.get(url)
        self.assertContains(response, self.admin_user.license_number)
