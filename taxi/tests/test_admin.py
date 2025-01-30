from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_superuser(
            username="Driver",
            password="<PASSWORD>",
            license_number="license_number"
        )

    def test_driver_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)

    def test_driver_detail_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        result = self.client.get(url)
        self.assertContains(result, self.driver.license_number)

    def test_driver_additional_info(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        result = self.client.get(url)
        self.assertContains(result, self.driver.first_name)
        self.assertContains(result, self.driver.last_name)
        self.assertContains(result, self.driver.license_number)
