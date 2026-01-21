from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="username", password="password"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="ABC12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver license number is displayed on driver list page
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver license number is displayed on driver detail page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        """
        Test that driver license number is displayed on driver add page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "License number")
