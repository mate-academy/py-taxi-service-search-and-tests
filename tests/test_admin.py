from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
            license_number="test licence number"
        )

    def test_driver_licence_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_licence_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)
