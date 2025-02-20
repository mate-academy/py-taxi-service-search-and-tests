from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class DriverAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user who can log in to the admin panel
        cls.user = get_user_model().objects.create_superuser(
            username="admin", password="password"
        )

        # Create a driver instance
        cls.driver = Driver.objects.create_user(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC123456",
        )

    def setUp(self):
        # Log in as the admin user
        self.client.login(username="admin", password="password")

    def test_driver_license_number_in_list_display(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))

        self.assertContains(response, "license_number")

    def test_driver_license_number_in_edit_page(self):
        response = self.client.get(
            reverse("admin:taxi_driver_change", args=[self.driver.pk])
        )

        self.assertContains(response, "license_number")

    def test_driver_license_number_in_add_page(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))

        self.assertContains(response, "license_number")

    def test_driver_admin_class_registers_correctly(self):
        driver_admin = site._registry.get(Driver)
        self.assertIsNotNone(driver_admin)

        expected_fields = (
            "username",
            "first_name",
            "last_name",
            "license_number"
        )
        for field in expected_fields:
            self.assertIn(field, driver_admin.list_display)

        found_in_fieldsets = any(
            "license_number" in section[1]["fields"]
            for section in driver_admin.fieldsets
        )
        self.assertTrue(
            found_in_fieldsets,
            "Field 'license_number' not found in fieldsets."
        )

        found_in_add_fieldsets = any(
            "license_number" in section[1]["fields"]
            for section in driver_admin.add_fieldsets
        )
        self.assertTrue(
            found_in_add_fieldsets,
            "Field 'license_number' not found in add_fieldsets."
        )
