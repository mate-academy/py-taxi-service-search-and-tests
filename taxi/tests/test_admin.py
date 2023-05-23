from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        # self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin",
            password="Admin_12345",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="Test driver",
            password="Driver_12345",
            license_number="XYR09876",
        )

    def driver_license_numbers_listed(self) -> None:
        """Test that driver's license_number is
        in list_display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        response_ = self.client.get(url)

        self.assertContains(response_, self.driver.license_number)

    def driver_detailed_license_numbers_listed(self) -> None:
        """Test that driver's license_number is
        in driver detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response_ = self.client.get(url)

        self.assertContains(response_, self.driver.license_number)

    def test_driver_create_license_number_listed(self):
        """Test that driver's license_number is
        in driver create admin page"""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "License number")
