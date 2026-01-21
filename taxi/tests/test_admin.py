from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, resolve


class DriverAdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="<PASSWORD>"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="<PASSWORD>", license_number="FFF12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_create_license_number_first_name_last_name_listed(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "Additional info")
        self.assertContains(res, "License number")
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")


class CarAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="<PASSWORD>"
        )
        self.client.force_login(self.admin_user)

    def test_search_field_present(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, "search")

    def test_filter_field_present(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, "Filter")
