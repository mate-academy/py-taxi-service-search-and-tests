from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Car
from ..admin import CarAdmin


class AdminSiteTest(TestCase):

    def setUp(self):
        self.site = AdminSite()

        self.admin_user = get_user_model().objects.create_superuser(
            username="test_username", password="test1234"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver_username",
            password="driver_1234",
            first_name="driver_name",
            last_name="driver_last_name",
            license_number="ASD12345",
        )

    def test_admin_driver_list_has_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_admin_change_page_displays_driver_license_number(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_admin_add_page_driver_displays_driver_fields(self):

        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "License number")
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")

    def test_car_admin_list_filer(self):
        url = reverse("admin:taxi_car_changelist")

        res = self.client.get(url)

        self.assertContains(res, "manufacturer")
