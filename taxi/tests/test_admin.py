from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create(
            username="test_user",
            password="1qazcde3",
            license_number="ABC12345"
        )

    def test_admin_site_license_number_displayed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)

    def test_admin_detail_license_number_displayed(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)

    def test_admin_add_license_number_displayed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
