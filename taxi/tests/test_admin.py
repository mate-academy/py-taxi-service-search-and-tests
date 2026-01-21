from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="Test license_number",

        )

    def test_driver_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_first_name_last_name_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )

        res = self.client.get(url)
        self.assertContains(res, self.driver.last_name)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.license_number)
