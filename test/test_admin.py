from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_name",
            password="admin_password",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_name",
            password="test_password",
            license_number="AAA12345",
        )

    def test_driver_license_number_display_on_admin_page(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_display_on_admin_detail_page(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_display_on_admin_add_page(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
        self.assertTrue(response, self.driver.license_number)
