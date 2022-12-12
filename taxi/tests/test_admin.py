from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3"
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
            license_number="IKL12341"
        )

    def test_driver_license(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_license_add(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "License number")
