from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            license_number="AMD12345"
        )

    def test_driver_list_display_contains_license_number(self):
        """
        Test that driver's license number
        is in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_fieldsets_contains_license_number(self):
        """
        Test that driver's license number
        is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fieldsets_contains_first_last_name_license_number(
            self
    ):
        """
        Test that driver's first_name, last_name, license number
        is in driver add admin page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
