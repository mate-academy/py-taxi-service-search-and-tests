from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="securepassword",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_changelist_displays_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_change_form_displays_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fields(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "license_number")
