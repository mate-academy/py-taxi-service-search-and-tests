from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admintest",
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="drivertest",
            license_number="ABC11111"
        )

    def test_driver_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        resp = self.client.get(url)
        self.assertContains(resp, self.driver.license_number)

    def test_driver_license_number_listed_on_driver_detail_page(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        resp = self.client.get(url)
        self.assertContains(resp, self.driver.license_number)

    def test_driver_license_number_add_to_driver_create_page(self) -> None:
        url = reverse("admin:taxi_driver_add")
        resp = self.client.get(url)
        self.assertContains(resp, "license_number")
