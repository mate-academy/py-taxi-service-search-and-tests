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
            username="test",
            password="1qazcde3",
            license_number="ABC12345"
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

    def test_driver_delete_success_url(self):
        view = DriverDeleteView()
        view.object = self.user
        self.assertEqual(view.get_success_url(), DRIVER_URL)

    def test_create_author(self):
        form_data = {
            "username": "new_user",
            "password1": "user55test",
            "password2": "user55test",
            "license_number": "ABC12346",
            "first_name": "First user",
            "last_name": "Last user",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
