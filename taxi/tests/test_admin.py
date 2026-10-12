from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.Driver = get_user_model().objects.create_user(
            username="driver",
            first_name="test_driver_name",
            last_name="test_driver_last_name",
            email="test_driver_email",
            license_number="AAA11111"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.Driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.Driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.Driver.license_number)
