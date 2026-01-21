from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123",
        )
        self.client.force_login(self.admin_user)
        self.driver = self.admin_user = get_user_model().objects.create_user(
            username="driver",
            password="test123",
            license_number="test54321"
        )

    def test_driver_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_add_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")

    def test_create_driver_without_license_number(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.post(url, {
            "username": "test",
            "password": "test1234",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
