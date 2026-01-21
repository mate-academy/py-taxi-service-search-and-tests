from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminPanelTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@localhost",
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="ASD12345",
        )

    def test_driver_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_deteil_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_deteil_add_license_number(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
