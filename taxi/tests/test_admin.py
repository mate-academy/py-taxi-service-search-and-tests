from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin6ge367",
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver83uau7",
            license_number="GFR76542",
        )

    def test_driver_license_number_listed(self):
        """Tests that license number is in list_display on admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(
            res,
            self.driver.license_number
        )

    def test_driver_detailed_license_number_listed(self):
        """Tests that license number is on driver detail admin page"""
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        res = self.client.get(url)

        self.assertContains(
            res,
            self.driver.license_number
        )
