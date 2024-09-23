from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.admin.sites import site
from django.urls import reverse

from taxi.models import Car
from taxi.admin import DriverAdmin, CarAdmin


class DriverAdminTest(TestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username="admin", password="<PASSWORD>"
        )
        self.client.force_login(admin_user)
        self.driver = get_user_model().objects.create(
            username="driver", password="<PASSWORD>", license_number="VBN12345"
        )
        self.admin_instance = DriverAdmin(get_user_model(), site)

    def test_list_display_contains_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertIn("license_number", self.admin_instance.list_display)
        self.assertContains(response, self.driver.license_number)

    def test_fieldsets_contains_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_add_fieldsets_contains_license_number(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "license_number")


class CarAdminTest(TestCase):
    def setUp(self):
        self.car_admin_instance = CarAdmin(Car, site)

    def test_search_fields_contains_model(self):
        self.assertIn("model", self.car_admin_instance.search_fields)

    def test_list_filter_contains_manufacturer(self):
        self.assertIn("manufacturer", self.car_admin_instance.list_filter)
