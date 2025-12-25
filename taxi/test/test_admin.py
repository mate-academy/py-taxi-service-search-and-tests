from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverAdminPanelTest(TestCase):
    def setUp(self):
        super_user = get_user_model().objects.create_superuser(
            username="test_name",
            password="password12345"
        )
        self.client.force_login(super_user)

        self.driver = get_user_model().objects.create_user(
            username="test_name_simple",
            password="passwords12345",
            first_name="first_name",
            last_name="last_name",
            license_number="ABC12345"
        )

    def test_admin_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_admin_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_admin_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
