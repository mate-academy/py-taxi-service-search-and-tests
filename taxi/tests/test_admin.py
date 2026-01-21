from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.tests import fixtures


class AdminSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def setUp(self):
        self.admin_user = get_user_model().objects.last()
        self.client.force_login(self.admin_user)

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")

        response = self.client.get(url)

        self.assertContains(response, self.admin_user.license_number)

    def test_driver_additional_fields_on_create_page(self):
        url = reverse("admin:taxi_driver_add")
        additional_fields = ["first_name", "last_name", "license_number"]

        response = self.client.get(url)

        for field in additional_fields:
            self.assertContains(response, field)

    def test_driver_license_number_field_on_edit_page(self):
        url = reverse("admin:taxi_driver_change", args=[self.admin_user.pk])

        res = self.client.get(url)

        self.assertContains(res, "license_number")

    def test_car_search_field_only_on_list_page_and_works(self):
        url = reverse("admin:taxi_car_changelist") + "?q=g"

        res = self.client.get(url)

        self.assertContains(res, 'name="q"', count=1)
        self.assertContains(res, "MG 5 II")
        self.assertContains(res, "Rising Auto ER6")
        self.assertNotContains(res, "Mitsubishi Eclipse")
        self.assertNotContains(res, "Mitsubishi Lancer")

    def test_car_filter_by_manufacturer_only_on_page_and_works(self):
        filter_ = "?manufacturer__id__exact=7"
        url = reverse("admin:taxi_car_changelist") + filter_

        response = self.client.get(url)

        self.assertContains(response, filter_, count=1)
        self.assertContains(response, "MG 5 II")
        self.assertContains(response, "Rising Auto ER6")
        self.assertNotContains(response, "Mitsubishi Eclipse")
        self.assertNotContains(response, "Mitsubishi Lancer")
