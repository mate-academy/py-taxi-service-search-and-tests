from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="test123123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="test_license_number",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
