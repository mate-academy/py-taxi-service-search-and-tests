from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAdminPanel(TestCase):
    def setUp(self) -> None:
        admin = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(admin)
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="testuser",
            license_number="ABC12345"
        )

    def test_driver_license_is_added_on_admin_page(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_is_listed_on_admin_page(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_correct_fields_added_in_driver_on_admin_page(self):
        add_user_url = reverse("admin:taxi_driver_add")
        response = self.client.get(add_user_url)

        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "License number:")
