from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="test1234",
            license_number="FRT12345"
        )

    def test_driver_license_number_listed(self):
        """Test that driver's license_number
        is in list_display on driver admin page"""

        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """Test that driver's license_number
        is on driver detail admin page"""

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        """Test that driver's license_number
        is on driver add admin page"""

        url = reverse("admin:taxi_driver_add")
        result = self.client.get(url)

        self.assertContains(result, "license_number")
