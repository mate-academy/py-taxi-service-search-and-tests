from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer
from taxi.views import (
    CarListView,
    CarDeleteView,
    CarUpdateView,
    CarCreateView
)

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany")
        self.car = Car.objects.create(
            model="test-car",
            manufacturer=self.manufacturer,
        )
        self.response = self.client.get(CAR_URL)

    def test_car_authenticated_user_access(self):
        self.assertEqual(self.response.status_code, 200)

    def test_manufacturer_paginate(self):
        self.assertEqual(CarListView.paginate_by, 5)

    def test_car_context_data(self):
        form = self.response.context["search_form"]
        self.assertIsInstance(form, CarSearchForm)
        self.assertEqual(form.initial["model"], "")

    def test_car_create_success_url(self):
        view = CarCreateView()
        view.object = self.car
        self.assertEqual(view.get_success_url(), CAR_URL)

    def test_car_update_success_url(self):
        view = CarUpdateView()
        view.object = self.car
        self.assertEqual(view.get_success_url(), CAR_URL)

    def test_car_delete_success_url(self):
        view = CarDeleteView()
        view.object = self.car
        self.assertEqual(view.get_success_url(), CAR_URL)
