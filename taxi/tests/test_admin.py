from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            license_number="ASD12345",
        )

    def test_driver_license_number_listed(self):
        """Test that driver's license number is in list_display
        on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """Test that driver's license number is in driver detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
