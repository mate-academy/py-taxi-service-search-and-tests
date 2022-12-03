from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="Arioh", password="9785699S"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="1234567S",
            license_number="SEB97856",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_license_and_names_listed(self):
        """Test driver`s license number,
        first and last name on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)

    def test_driver_detail_license_and_names_listed(self):
        """Test driver`s license number,
        first and last name on driver detail admin page"""

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)
