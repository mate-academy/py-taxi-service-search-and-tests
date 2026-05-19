from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            license_number="ADM12345",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test1234",
            first_name="John",
            last_name="Doe",
            license_number="TST12345",
        )

    def test_driver_listed(self):
        """Driver list page shows username, first_name,
        last_name, license_number"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
        self.assertContains(response, self.driver.username)

    def test_driver_detail_page(self):
        """Driver change page loads correctly"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_driver_add_page(self):
        """Driver add page loads and contains license_number field"""
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
