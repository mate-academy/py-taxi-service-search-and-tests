from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test12345",

        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test1234567",
            license_number="ADM12345"
        )

    def test_driver_license_number_listes(self):
        url = reverse("admin:taxi_driver_changelist")
        self.assertContains(self.client.get(url), self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )

        self.assertContains(
            self.client.get(url),
            self.driver.license_number
        )
