from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="<PASSWORD>",
            license_number="ASD12345",
        )

    def test_driver_license_number(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_admin(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
