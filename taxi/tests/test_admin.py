from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123456"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="author123456",
            license_number="AAA12345"
        )

    def test_driver_licence_number_listed(self):
        """Test that driver's license number is
        listed in list_display in admin page"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_licence_number_listed(self):
        """Test that driver's license number is
        listed in driver detail in admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_page_contains_licence_number_listed(self):
        """Test that driver's license number
        field is listed in add page in admin page"""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "License number:")
