from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="strong_password",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create(
            username="awesome_username",
            first_name="awesome_name",
            last_name="awesome_last_name",
            password="strongestPassword",
            license_number="ABC12345"
        )

    def test_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_license_number_detail_listed(self) -> None:
        url = reverse(
            "admin:taxi_driver_change", args=[self.driver.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
