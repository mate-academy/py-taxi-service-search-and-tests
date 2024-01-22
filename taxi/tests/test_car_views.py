from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import CarModelSearchForm
from taxi.models import Car, Manufacturer


class CarViewsTest(TestCase):
    CAR_LIST_URL = reverse("taxi:car-list")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
            password="testpassword",
        )

        self.client = Client()
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
        )
        for _id in range(15):
            Car.objects.create(
                model=f"Test model {_id}",
                manufacturer=self.manufacturer
            )

    def test_list_if_not_login(self):
        self.client.logout()
        res = self.client.get(self.CAR_LIST_URL)
        self.assertRedirects(res, "/accounts/login/?next=/cars/")

    def test_list_view_if_logged_in(self):
        res = self.client.get(self.CAR_LIST_URL)

        self.assertEqual(str(res.context["user"]), str(self.user))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_list_view_pagination(self):
        res = self.client.get(self.CAR_LIST_URL)

        self.assertTrue("is_paginated" in res.context)
        self.assertEqual(len(res.context["car_list"]), 5)

    def test_list_view_search(self):
        car = Car.objects.create(
            model="rsq8",
            manufacturer=self.manufacturer
        )
        res = self.client.get("/cars/?model=r")

        self.assertTrue("search_form" in res.context)
        self.assertIsInstance(res.context["search_form"], CarModelSearchForm)
        self.assertEqual(res.context["search_form"].initial["model"], "r")
        self.assertEqual(len(res.context["car_list"]), 1)
        self.assertEqual(res.context["car_list"][0], car)

    def test_list_view_invalid_search(self):
        res = self.client.get("/cars/?name=")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 5)
        self.assertFalse(res.context["search_form"].is_valid())
