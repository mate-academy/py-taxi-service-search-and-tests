from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin", password="abc123"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="author", password="asdf123", license_number="QWE132"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        resp = self.client.get(url)
        self.assertContains(resp, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        resp = self.client.get(url)
        self.assertContains(resp, self.driver.license_number)

    def test_driver_created(self):
        url = reverse("admin:taxi_driver_add")
        resp = self.client.get(url)
        self.assertContains(resp, "License number")
