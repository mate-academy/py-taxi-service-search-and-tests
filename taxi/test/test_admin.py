from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number"
        )

    def test_drivers_license_listed(self):
        """Test that driver's license_number is in
        listed on drivers admin page"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_drivers_detail_license_listed(self):
        """Test that driver's license_number is in
        listed on drivers detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_drivers_additional_info_add_fieldsets(self):
        """Test that driver's additional info is in
         listed on drivers add admin page"""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
