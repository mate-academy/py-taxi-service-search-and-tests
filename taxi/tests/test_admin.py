from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_password",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password",
            license_number="test_license_number",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, "license_number")

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertContains(response, "license_number")

    def test_driver_add_first_name_last_name_license_number(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
