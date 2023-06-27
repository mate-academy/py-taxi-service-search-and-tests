from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234,"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="username",
            first_name="Test first",
            last_name="Test last",
            password="password",
            license_number="TES12345",
        )

    def test_driver_license_number_listed(self):
        """Test driver license_number in list_display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_licence_number_listed(self):
        """Test that driver license_number in detailed on driver admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_first_name_listed(self):
        """Test that driver first_name in detailed on driver admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)

    def test_driver_detailed_last_name_listed(self):
        """Test that driver last_name in detailed on driver admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.last_name)
