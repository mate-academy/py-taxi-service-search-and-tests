from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )

    def test_driver_list_display_license_number(self):
        """Test that license_number is displayed in DriverAdmin list."""
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        """Test that license_number is included in add_fieldsets."""
        response = self.client.get(reverse("admin:taxi_driver_add"))
        self.assertContains(response, "license_number")
