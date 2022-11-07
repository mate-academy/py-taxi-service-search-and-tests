from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="TestUsernameDriver",
            password="qwe123",
            license_number="ABC12345"
        )

    def test_driver_license_number(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))

        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_detailed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
