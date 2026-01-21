from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            "admi1",
            "2wsxvfr4"
        )
        self.client.force_login(self.admin)

        self.driver = get_user_model().objects.create_user(
            username="test1",
            password="password123",
            license_number="TET12332"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "License number:")
