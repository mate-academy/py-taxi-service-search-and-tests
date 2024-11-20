from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin123",
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver123",
            license_number="ASD12345",
        )

    def test_driver_license_number_displayed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_displayed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id],
        )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
