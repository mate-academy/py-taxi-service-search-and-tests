from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car


class DriverAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="user",
            password="testuser",
            license_number="ABC12345",
            first_name="User",
            last_name="Userovich",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change",
                      args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_add_detail_license_number_first_last_name(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")


class CarAdminSiteTests(TestCase):
    def test_search_fields(self):
        self.assertIn("model", site._registry[Car].search_fields)

    def test_list_filter(self):
        from django.contrib.admin import site
        self.assertIn("manufacturer", site._registry[Car].list_filter)
