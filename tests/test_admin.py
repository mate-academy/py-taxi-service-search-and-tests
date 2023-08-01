from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="12345admin"
        )

        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create(
            username="driver",
            password="driver12345",
            license_number="ABC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_create_additional_fields_listed(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.driver.license_number = ""

        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
        self.assertContains(res, self.driver.license_number)
