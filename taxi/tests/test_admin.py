from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car


class AdminPanelTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin", password="test1234"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create(
            username="test", password="test5432", license_number="TES12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_create_additional_info_included(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "license_number")

    def test_admin_car_search_field(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, "searchbar")

    """
    How to check for list_filter?
    """
