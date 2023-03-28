from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, "ABC12345")

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, "License number:")

    def test_driver_add_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        custom_fields = ("License number:", "First name:", "Last name:")

        for custom_field in custom_fields:
            self.assertContains(response, custom_field)
