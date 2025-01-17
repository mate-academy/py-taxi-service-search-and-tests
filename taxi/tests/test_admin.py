from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_superuser(
            username="driver",
            password="testpassword",
            license_number="testlicense",
        )

    def test_driver_license_number_listed(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_license_number_in_update(self):
        url = reverse("taxi:driver-update", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
