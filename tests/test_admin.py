from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin12",
            password="fgrhe43FG35",
            license_number="SDF34654"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="dsgsdg363AS25",
            license_number="DLF45980",
            last_name="Test_Last"
        )

    def test_driver_last_name_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.last_name)

    def test_driver_last_name_detail_listed(self):
        url = reverse("admin:taxi_driver_change", args=(self.driver.id,))
        response = self.client.get(url)
        self.assertContains(response, self.driver.last_name)
