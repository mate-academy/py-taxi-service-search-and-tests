from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.user = get_user_model().objects.create(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)

    def test_driver_license_num_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.license_number)

    def test_driver_detail_license_num_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertContains(res, self.user.license_number)
