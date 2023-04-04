from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Car, Manufacturer
from django.contrib.auth import get_user_model


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            license_number="ABC12345"
        )

    def test_driver_license_on_admin_page(self):
        url = reverse("admin:taxi_driver_changelist")

        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_on_admin_add_page(self):
        url = reverse("admin:taxi_driver_add")

        response = self.client.get(url)
        self.assertContains(response, "License number")
