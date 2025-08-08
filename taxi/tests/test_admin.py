from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
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
            license_number="ABC12345"
        )

    def test_license_number_listed(self):
        """Test that driver's license number is displayed in admin list view"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_change_page(self):
        """Test that the driver change page works and is accessible"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_driver_add_page_has_license_number(self):
        """
            Test that the license number field is shown
            on the add driver page
            """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
