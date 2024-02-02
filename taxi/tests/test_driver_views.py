from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi import forms
from taxi.models import Car, Driver, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

        number_of_drivers = 12

        for driver_id in range(number_of_drivers):
            Driver.objects.create_user(
                username=f"driver {driver_id}",
                password=f"test_driver {driver_id}",
                license_number=f"test_license_number{driver_id}",
            )

    def test_view_url_exists(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_view_have_search_form_context(self):
        response = self.client.get(DRIVER_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            forms.DriverSearchForm
        )

    def test_view_have_creation_form_context(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertIsInstance(
            response.context["form"],
            forms.DriverCreationForm
        )

    def test_view_have_update_license_number_form_context(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[Driver.objects.first().pk])
        )
        self.assertIsInstance(
            response.context["form"],
            forms.DriverLicenseUpdateForm
        )

    def test_existing_pagination(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_pagination_paged(self):
        response = self.client.get(DRIVER_URL + "?page=3")
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_correct_query_set(self):
        response = self.client.get(DRIVER_URL, {"username": "driver 3"})
        self.assertContains(response, "driver 3")
        self.assertNotContains(response, "driver 4")

    def test_driver_detail_view_exist(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[Driver.objects.first().pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_update_license_number_driver_detail_view_exist(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[Driver.objects.first().pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_car_detail_view_exist(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[Driver.objects.first().pk])
        )
        self.assertEqual(response.status_code, 200)
