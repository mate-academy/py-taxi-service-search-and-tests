from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.views import (
    DriverListView,
    DriverDeleteView,
    DriverCreateView,
    DriverLicenseUpdateView,
)

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 302)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass1325",
            license_number="QWE78945"
        )
        self.client.force_login(self.user)
        self.response = self.client.get(DRIVER_URL)

    def test_driver_authenticated_user_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_driver_paginate(self):
        self.assertEqual(DriverListView.paginate_by, 5)

    def test_driver_context_data(self):
        form = self.response.context["search_form"]
        self.assertIsInstance(form, DriverSearchForm)
        self.assertEqual(form.initial["username"], "")

    def test_driver_license_update_success_url(self):
        view = DriverLicenseUpdateView()
        view.object = self.user
        self.assertEqual(view.get_success_url(), DRIVER_URL)
