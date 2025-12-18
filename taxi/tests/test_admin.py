from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="password",
            first_name="Driver",
            last_name="Driver",
            license_number="ABC12345",
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_first_last_name_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)


class CarAdminTest(TestCase):
    def test_car_admin_search_fields(self):
        car_admin = admin.site._registry[Car]
        self.assertEqual(car_admin.search_fields, ("model",))

    def test_car_admin_list_filter(self):
        car_admin = admin.site._registry[Car]
        self.assertEqual(car_admin.list_filter, ("manufacturer",))

    def test_manufacturer_is_registered(self):
        self.assertIn(Manufacturer, admin.site._registry)
