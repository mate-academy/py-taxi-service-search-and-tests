from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
            license_number="ABC12345"
        )

    def test_driver_license_listed(self):
        """Test that driver's license number is in list_display
        on the driver admin page"""

        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.author.license_number)

    def test_admin_driver_license_change(self):
        """Test that driver's license number is on the driver detail page."""
        url = reverse("admin:taxi_driver_change", args=[self.author.id])
        response = self.client.get(url)

        self.assertContains(response, self.author.license_number)

    def test_admin_driver_license_add(self):
        """Test that driver's license number is on the driver creation page."""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, 'name=\"license_number\"')
