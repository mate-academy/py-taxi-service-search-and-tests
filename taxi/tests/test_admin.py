from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="test",
            password="testdriver",
            license_number="ABC12345",
        )

    def test_driver_license_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
