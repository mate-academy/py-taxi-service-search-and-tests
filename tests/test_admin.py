from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create(
            username="driver",
            password="driver1234",
            license_number="ABC12345",
        )

    def test_driver_license_number_listed(self):
        """Test that driver's license number
        is in list display on admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """Test that driver's license number
        is detail on admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_page_contains_additional_info_fields(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
