from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="ABC12345",
        )

    def test_driver_license_number_listed(self):
        """Driver license number Listed on admin page"""
        self.assertContains(
            self.client.get(reverse("admin:taxi_driver_changelist")),
            self.driver.license_number,
        )

    def test_driver_detail_license_number_listed(self):
        """Driver license number Listed on driver detail admin page"""
        self.assertContains(
            self.client.get(reverse("admin:taxi_driver_change", args=[self.driver.id])),
            self.driver.license_number,
        )
