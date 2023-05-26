from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="author123",
            license_number="ABCD12345"
        )

    def test_driver_license_number_listed(self):
        """Tests that driver`s license number is in list
        display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """Tests that driver`s license number is an detail driver admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        """Tests that driver`s license number is add to admin page"""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "License number:")
