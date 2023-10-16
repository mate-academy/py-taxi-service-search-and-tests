from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="12testpass34"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="lewis.hamilton",
            password="34testpass12",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "License number")
