from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="12345"
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="12345",
            license_number="test license"
        )

    def test_driver_license_number_in_admin_panel(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_detail_driver_license_number_in_admin_panel(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_create_driver_license_number_in_admin_panel(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "license_number")
