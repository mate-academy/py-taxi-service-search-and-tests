from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin",
            password="Admin_12345",
        )
        self.client.forse_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="Test driver",
            password="Driver_12345",
            license_number="XYR09876",
        )

    def driver_license_numbers_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response_ = self.client.get(url)

        self.assertContains(response_, self.driver.license_number)
