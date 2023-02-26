from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverAdminTests(TestCase):
    def setUp(self):
        self.admin_ = get_user_model().objects.create_superuser(
            username="admin123",
            password="admintestpass"
        )
        self.client.force_login(self.admin_)
        self.driver = get_user_model().objects.create_user(
            username="admin1223",
            password="admintestspass",
            first_name="Volkswagen",
            last_name="Germany",
            license_number="VOL12345"
        )

    def test_driver_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)
