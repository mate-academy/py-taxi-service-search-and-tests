from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="ABC12345",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_first_name_last_name_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        data = {
            "username": "new_driver",
            "password1": "password",
            "password2": "password",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        response = self.client.post(url, data)
        self.assertContains(response, "ABC12345")
        self.assertContains(response, "New")
        self.assertContains(response, "Driver")
