from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer
from taxi.views import (
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView
)

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany")
        self.response = self.client.get(MANUFACTURER_URL)

    def test_manufacturer_template_used(self):
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")

    def test_manufacturer_authenticated_user_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_context(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_paginate(self):
        self.assertEqual(ManufacturerListView.paginate_by, 5)

    def test_manufacturer_context_data(self):
        form = self.response.context["search_form"]
        self.assertIsInstance(form, ManufacturerSearchForm)
        self.assertEqual(form.initial["name"], "")

    def test_manufacturer_create_success_url(self):
        view = ManufacturerCreateView()
        view.object = self.manufacturer
        self.assertEqual(view.get_success_url(), MANUFACTURER_URL)

    def test_manufacturer_update_success_url(self):
        view = ManufacturerUpdateView()
        view.object = self.manufacturer
        self.assertEqual(view.get_success_url(), MANUFACTURER_URL)

    def test_manufacturer_delete_success_url(self):
        view = ManufacturerDeleteView()
        view.object = self.manufacturer
        self.assertEqual(view.get_success_url(), MANUFACTURER_URL)
