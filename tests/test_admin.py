from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="admin12345",
            license_number="RDM12345"
        )

    def test_driver_license_number_listed(self):
        """Test that driver license number
        is in list_display driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """Test that driver license number
        is in driver detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_add_driver_first_last_name_license_number_listed(self):
        """Test that driver license number
        is in driver detail admin page"""
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "License number")
